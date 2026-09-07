---
tags: [deck-slide, kpmg-deck, exported]
slide: 11
layout: Title only_Blank
---

# A long series needs few labels

> Slide 11 of 11, on layout `Title only_Blank`.

**Twenty quarters plotted and four labelled, which is the only way a dense time series stays readable at 8pt**

## Exhibit 1

**Sparse category labels keep a twenty-point series legible**

*Illustrative series, units, Q1 2021 - Q4 2025*

- Chart ID: `selftest_sparse`
- Series: Series
- Categories (20): Q1 2021, ​​, ​​​, ​​​​, ​​​​​, ​​​​​​, ​​​​​​​, ​​​​​​​​, Q1 2023, ​​​​​​​​​​, ​​​​​​​​​​​, ​​​​​​​​​​​​ ...
- Position: 2.73, 4.87 cm, 13.70 x 10.75 cm

## The read

- sparse_labels() blanks the categories the axis should not print, and leaves every plotted point where it was
- A plain empty string will not do it, because PowerPoint collapses duplicate category names and the series loses points
- A run of ordinary spaces will not do it either: the label stub still draws, and the axis grows a row of tick marks
- plot_rect pins the plot area, so a chart with many categories cannot be squashed into the top of its own frame by the renderer

## Sources

Source: kpmg-deck self-test, illustrative.

## Related

- [[00 — Slide Index]]
