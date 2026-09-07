"""Self-deploying KPMG brand fonts.

House note, 25 August 2026: "Embed the KPMG bold font inside the skill so it auto
deploys every time and self deploys... self contained... on all the fonts
please, yeah not to git, but for work use."

So the skill carries all nine faces in `assets/fonts/` and installs them into
the user font directory the first time a deck is built. A new machine needs no
setup step and no checklist: clone or copy the skill, build a deck, and the
titles come out in KPMG Bold.

**The binaries are never committed.** They are licensed to KPMG by Commercial
Type, and the vault this skill lives in pushes to GitHub, so `assets/fonts/`
is in `.gitignore` and `check_not_tracked()` below fails loudly if that ever
stops being true. Self-contained on disk is the goal; redistribution is not.

Called automatically by `deckkit.new_deck()`. Safe to call repeatedly: it
copies only what is missing or stale, and it never touches a system font
directory, only the per-user one.
"""
import os
import platform
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLED = os.path.normpath(os.path.join(HERE, "..", "assets", "fonts"))

# The off-vault master copy, kept per machine outside any repository. Used as a
# fallback seed when the bundled folder is empty, which is what a fresh clone
# looks like: git carries the skill, never the fonts.
VENDOR = os.path.expanduser(
    "~/Library/Application Support/Artemis/fonts-vendor/kpmg")


def user_font_dir():
    system = platform.system()
    if system == "Darwin":
        return os.path.expanduser("~/Library/Fonts")
    if system == "Windows":
        return os.path.join(os.environ.get("LOCALAPPDATA", ""),
                            "Microsoft", "Windows", "Fonts")
    return os.path.expanduser("~/.local/share/fonts")


def bundled_faces(directory=None):
    d = directory or BUNDLED
    if not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d)
                  if f.lower().endswith((".ttf", ".otf")))


def ensure_installed(verbose=False, directory=None):
    """Install any bundled face the user font directory does not already have.

    Returns (installed, already_present, missing_from_bundle). Never raises on
    a font that cannot be copied: a deck that builds in Arial with a warning is
    better than a deck that does not build, and `deckkit.check()` plus the
    render-time font probe will catch the substitution anyway.
    """
    src = directory or BUNDLED
    if not bundled_faces(src) and os.path.isdir(VENDOR):
        # Fresh clone: seed the bundle from this machine's licensed copy.
        os.makedirs(src, exist_ok=True)
        for f in bundled_faces(VENDOR):
            try:
                shutil.copy2(os.path.join(VENDOR, f), os.path.join(src, f))
            except OSError:
                pass

    dest_dir = user_font_dir()
    installed, present = [], []
    faces = bundled_faces(src)
    if not faces:
        if verbose:
            print("  fonts: none bundled and no vendor copy found; titles will "
                  "fall back to Arial Bold")
        return installed, present, True

    try:
        os.makedirs(dest_dir, exist_ok=True)
    except OSError:
        return installed, present, False

    for face in faces:
        s_path = os.path.join(src, face)
        d_path = os.path.join(dest_dir, face)
        try:
            if (os.path.exists(d_path)
                    and os.path.getsize(d_path) == os.path.getsize(s_path)):
                present.append(face)
                continue
            shutil.copy2(s_path, d_path)
            installed.append(face)
        except OSError:
            continue

    if installed and platform.system() == "Darwin":
        # Nudge the font server so the face is usable in this session rather
        # than after a relaunch. Best effort; absence is not an error.
        try:
            subprocess.run(["atsutil", "databases", "-remove"],
                           capture_output=True, timeout=20)
        except (OSError, subprocess.SubprocessError):
            pass

    if verbose:
        if installed:
            print("  fonts: installed %d face(s) to %s"
                  % (len(installed), dest_dir))
        else:
            print("  fonts: %d face(s) already present" % len(present))
    return installed, present, False


def check_not_tracked(repo_root=None):
    """Fail loudly if the licensed binaries have become git-tracked.

    The whole arrangement rests on `assets/fonts/` being ignored. If a future
    .gitignore edit breaks that, the next push redistributes a commercial
    licence, so this is checked rather than assumed.
    """
    root = repo_root or os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
    try:
        out = subprocess.run(
            ["git", "-C", root, "ls-files", "--", "*.ttf", "*.otf"],
            capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return []
    tracked = [l for l in out.stdout.splitlines() if l.strip()]
    if tracked:
        print("  ! FONT LICENCE RISK: %d font file(s) are tracked by git and "
              "will be pushed. They are licensed to KPMG by Commercial Type "
              "and must not be redistributed. Add them to .gitignore and run "
              "git rm --cached." % len(tracked))
        for t in tracked[:5]:
            print("    %s" % t)
    return tracked


def report():
    faces = bundled_faces()
    dest = user_font_dir()
    have = [f for f in faces if os.path.exists(os.path.join(dest, f))]
    return {"bundled": len(faces), "installed": len(have), "dir": dest,
            "tracked_by_git": len(check_not_tracked())}
