"""SVG icons that stay vector, and stay recolourable, inside the deck.

the review note, 25 August 2026: icons are currently placed as pictures, and
should instead be SVG so the fill colours can be changed easily.

A picture cannot be recoloured. An SVG placed the way PowerPoint itself places
one can: PowerPoint 2016 and later store an SVG as a second blip inside the
picture's fill, alongside a raster fallback, and offer "Convert to Shape" and
"Graphics Fill" on it. python-pptx has no API for that, so `place()` writes the
same XML PowerPoint writes:

    <a:blip r:embed="rIdPng">
      <a:extLst>
        <a:ext uri="{96DAC541-7B7A-43D3-8B79-37D633B846F1}">
          <asvg:svgBlip r:embed="rIdSvg"/>
        </a:ext>
      </a:extLst>
    </a:blip>

`recolour()` rewrites the SVG's own fills before it goes in, so a deck can be
built in palette without anyone opening PowerPoint at all.

The raster fallback is produced with LibreOffice, which the skill already needs
for its render pass. Without it, `place()` refuses rather than silently
inserting a picture that cannot be recoloured, because a silent downgrade is
the exact failure being fixed here.
"""
import os
import re
import subprocess
import tempfile

from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.opc.package import Part
from pptx.opc.packuri import PackURI
from pptx.oxml.ns import _nsmap, qn
from pptx.util import Cm

from deckkit import (CM, DARK_BLUE, KPMG_BLUE, COBALT, PACIFIC, LIGHT_BLUE,
                     WHITE, GREY)

# The Microsoft SVG extension namespace, and the GUID that marks the extension.
_nsmap.setdefault("asvg", "http://schemas.microsoft.com/office/drawing/2016/SVG/main")
SVG_EXT_URI = "{96DAC541-7B7A-43D3-8B79-37D633B846F1}"

HERE = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.normpath(os.path.join(HERE, "..", "assets", "icons"))
CACHE_DIR = os.path.join(tempfile.gettempdir(), "kpmg-deck-icon-cache")

_COLOUR_ATTR = re.compile(r'(fill|stroke)\s*=\s*"(?!none)(#[0-9A-Fa-f]{3,8}|'
                          r'currentColor|[a-zA-Z]+)"')
_COLOUR_STYLE = re.compile(r'(fill|stroke)\s*:\s*(?!none)(#[0-9A-Fa-f]{3,8}|'
                           r'currentColor|[a-zA-Z]+)')


def recolour(svg_text, colour):
    """Set every non-`none` fill and stroke in an SVG to one palette colour."""
    hexv = "#%s" % str(colour)
    out = _COLOUR_ATTR.sub(lambda m: '%s="%s"' % (m.group(1), hexv), svg_text)
    out = _COLOUR_STYLE.sub(lambda m: '%s:%s' % (m.group(1), hexv), out)
    if 'fill=' not in out and 'fill:' not in out:
        out = out.replace("<svg", '<svg fill="%s"' % hexv, 1)
    return out


def _rasterise(svg_path, png_path, width_px=512):
    """PNG fallback via LibreOffice. Raises if it is not installed."""
    if os.path.exists(png_path) and os.path.getmtime(png_path) >= os.path.getmtime(svg_path):
        return png_path
    soffice = None
    for cand in ("soffice", "/Applications/LibreOffice.app/Contents/MacOS/soffice"):
        try:
            subprocess.run([cand, "--version"], capture_output=True, timeout=60)
            soffice = cand
            break
        except (OSError, subprocess.SubprocessError):
            continue
    if soffice is None:
        raise RuntimeError(
            "icons.place() needs LibreOffice to write the raster fallback that "
            "PowerPoint requires alongside an SVG. Install it "
            "(brew install --cask libreoffice), or place the icon as a plain "
            "picture and accept that it cannot be recoloured.")
    outdir = os.path.dirname(png_path)
    os.makedirs(outdir, exist_ok=True)
    subprocess.run([soffice, "--headless", "--convert-to",
                    "png:draw_png_Export", "--outdir", outdir, svg_path],
                   capture_output=True, timeout=180)
    produced = os.path.join(
        outdir, os.path.splitext(os.path.basename(svg_path))[0] + ".png")
    if not os.path.exists(produced):
        raise RuntimeError("LibreOffice did not produce a PNG for %s" % svg_path)
    if produced != png_path:
        os.replace(produced, png_path)
    return png_path


_svg_counter = [0]


def _add_svg_part(slide_part, svg_bytes):
    _svg_counter[0] += 1
    partname = PackURI("/ppt/media/icon%d.svg" % _svg_counter[0])
    part = Part(partname, "image/svg+xml", slide_part.package, svg_bytes)
    return slide_part.relate_to(part, RT.IMAGE)


def place(slide, svg, left, top, size, *, colour=KPMG_BLUE, name=None):
    """Put an SVG icon on a slide as a true vector picture, in centimetres.

    `svg` is a path to an .svg file, the raw SVG text, or the name of one of
    the icons bundled in assets/icons. `size` is the square edge in cm.
    """
    if isinstance(svg, str) and svg.strip().startswith("<"):
        svg_text, stem = svg, "inline%d" % (_svg_counter[0] + 1)
    else:
        path = svg if os.path.exists(svg) else os.path.join(ICON_DIR, "%s.svg" % svg)
        if not os.path.exists(path):
            raise FileNotFoundError(
                "no icon %r. Bundled icons: %s" % (svg, sorted(available())))
        svg_text = open(path, encoding="utf-8").read()
        stem = os.path.splitext(os.path.basename(path))[0]

    if colour is not None:
        svg_text = recolour(svg_text, colour)

    os.makedirs(CACHE_DIR, exist_ok=True)
    key = "%s_%s" % (stem, str(colour))
    svg_path = os.path.join(CACHE_DIR, key + ".svg")
    with open(svg_path, "w", encoding="utf-8") as fh:
        fh.write(svg_text)
    png_path = _rasterise(svg_path, os.path.join(CACHE_DIR, key + ".png"))

    pic = slide.shapes.add_picture(png_path, CM(left), CM(top),
                                   CM(size), CM(size))
    pic.name = name or ("ICON_%s" % stem.upper())

    rId_svg = _add_svg_part(slide.part, svg_text.encode("utf-8"))
    blip = pic._element.blipFill.find(qn("a:blip"))
    extLst = blip.find(qn("a:extLst"))
    if extLst is None:
        extLst = blip.makeelement(qn("a:extLst"), {})
        blip.append(extLst)
    ext = extLst.makeelement(qn("a:ext"), {"uri": SVG_EXT_URI})
    svg_blip = ext.makeelement(qn("asvg:svgBlip"), {qn("r:embed"): rId_svg})
    ext.append(svg_blip)
    extLst.append(ext)
    return pic


def available():
    if not os.path.isdir(ICON_DIR):
        return []
    return sorted(os.path.splitext(f)[0] for f in os.listdir(ICON_DIR)
                  if f.endswith(".svg"))


# ---------------------------------------------------------------------------
# A starter set, drawn as single-path line icons on a 24 unit grid so they
# recolour cleanly and stay legible at 0.8 cm. This is a stand-in: the firm's
# own approved icon set has to be dropped into assets/icons to replace it.
# ---------------------------------------------------------------------------
STARTER = {
    "cost": "M12 2v20M17 6.5c0-2-2.2-3-5-3s-5 1-5 3 2 2.8 5 3.5 5 1.5 5 3.5-2.2 3-5 3-5-1-5-3",
    "time": "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 6v6l4 2",
    "target": "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10zM12 13a1 1 0 1 0 0-2 1 1 0 0 0 0 2z",
    "growth": "M3 17l6-6 4 4 8-8M15 7h6v6",
    "decline": "M3 7l6 6 4-4 8 8M15 17h6v-6",
    "risk": "M12 3L2 20h20L12 3zM12 9v5M12 17h.01",
    "network": "M6 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zM18 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zM12 21a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zM7.5 6.5h9M7 7.5l4 8M17 7.5l-4 8",
    "shield": "M12 3l8 3v6c0 5-3.4 8.3-8 9.5C7.4 20.3 4 17 4 12V6l8-3z",
    "balance": "M12 3v18M5 21h14M4 8h16M4 8l-2.5 6a3.5 3.5 0 0 0 5 0L4 8zM20 8l-2.5 6a3.5 3.5 0 0 0 5 0L20 8z",
    "document": "M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8l-5-5zM14 3v5h5M9 13h6M9 17h6",
    "search": "M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16zM21 21l-4.3-4.3",
    "flag": "M5 21V4M5 4h11l-2 3.5L16 11H5",
}

_TEMPLATE = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
             'width="96" height="96" fill="none" stroke="#00338D" '
             'stroke-width="1.6" stroke-linecap="round" '
             'stroke-linejoin="round"><path d="{d}"/></svg>')


def install_starter_set(directory=None, force=False):
    """Write the starter icons to assets/icons. Never overwrites by default."""
    directory = directory or ICON_DIR
    os.makedirs(directory, exist_ok=True)
    written = []
    for name, d in STARTER.items():
        path = os.path.join(directory, "%s.svg" % name)
        if os.path.exists(path) and not force:
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(_TEMPLATE.format(d=d))
        written.append(name)
    return written
