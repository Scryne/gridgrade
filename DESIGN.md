---
version: alpha
name: GridGrade
description: US electricity prices and utility report cards; public-interest data reference, light theme, report-card identity.
colors:
  paper: "#FAF8F3"
  surface: "#FFFFFF"
  ink: "#17181C"
  muted: "#5B616B"
  line: "#E3DED3"
  primary: "#1F4FD1"
  wire: "#F2B705"
  cheaper: "#1F6FB2"
  pricier: "#D2611C"
  grade-a: "#1E8550"
  grade-b: "#467A20"
  grade-c: "#C99A00"
  grade-d: "#B4500F"
  grade-f: "#C2302A"
typography:
  display:
    fontFamily: Fraunces
    fontWeight: 650
    fontSize: 44px
    lineHeight: 1.08
  heading:
    fontFamily: Fraunces
    fontWeight: 600
    fontSize: 26px
    lineHeight: 1.2
  body:
    fontFamily: Inter
    fontWeight: 400
    fontSize: 17px
    lineHeight: 1.6
  data:
    fontFamily: Inter
    fontWeight: 600
    fontSize: 15px
rounded:
  card: 10px
  badge: 8px
spacing:
  gutter: 16px
  section: 56px
---

# GridGrade

## Overview

A public-interest reference, not a startup landing page. Readers arrive from search with one question ("what does
electricity cost here?", "who supplies my county?") and must get the number in the first screen, then the context.

- **Mood:** report card meets newspaper data desk. Calm paper background, ink text, numbers set large and tabular.
- **Distinctive detail:** the letter grade badge. Every utility gets one, styled like a stamped report-card mark, always
  accompanied by the two sub-grades (price, reliability) so the letter is never a black box.

The global dark glassmorphism default does not apply: this is a light, ad-supported reading site where contrast and
scan speed matter more than atmosphere.

## Colors

Paper and ink carry the page; one warm accent (`wire`, a live-wire yellow) appears only as a thin rule and the logo mark.
Maps and comparisons use a blue/orange diverging pair (`cheaper`/`pricier`) that stays distinguishable for red-green color
blindness. Grade colors run green to red but every badge also shows the letter, so color is never the only signal.
`grade-c` and `wire` take dark text; the rest take white. Every grade color meets 4.5:1 with its text (B and D were darkened
after an axe audit on 2026-10-24). Increase/decrease figures in tables use darker text tones (#A9480F, cheaper blue) for the same reason.

## Typography

Fraunces for headlines gives editorial authority; Inter for everything else. All figures use tabular numerals so columns
align. The hero number on each page is the largest element on the screen.

## Components

- **Answer box:** first block on every page; the headline number, its unit, period and a one-line comparison.
- **Grade badge:** square, letter only, sub-grades listed beside it in small text.
- **Charts:** server-rendered SVG, no JavaScript; line for price over time, horizontal bars for rankings; every chart has a
  text summary and a data table nearby.
- **Tile map:** one square per state, colored on the diverging scale relative to the US average, each tile a link.
- **Ad slot:** fixed-height reserved box between sections, never above the answer box, labeled "Advertisement".

## Do's and Don'ts

- Do show the data period and source next to every number.
- Do keep the answer box above any ad.
- Don't use stock photos, gradients, glass, or decorative icons.
- Don't present a grade without its method link.
