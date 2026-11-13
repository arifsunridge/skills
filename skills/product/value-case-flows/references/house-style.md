# Sunridge House Style for flows

## Tokens (also in `scripts/svgkit.py` and the page CSS)

| Token | Hex | Use |
|---|---|---|
| Olive ink | #535349 | Titles, arrows, step numbers |
| Olive | #61664E | Box strokes, section rules |
| Gold | #D8A45F | Accent only: the title bar "\|", D markers, callouts |
| Sage light | #DDE5DC | The app, and the After column |
| Paper | #F7F5F0 | Systems, lane label cells, panels, the page header band |
| Ink | #2D2D2D | Body text |
| Grey | #6F6F6F | Sub-lines, source line, keyed-by-a-person arrows |
| Red | #B5543C | Before markers (retyped, guessed) |
| Green | #7D8F5E | After markers (kept) |

Type: Libre Baskerville for titles as "Section | *Topic*" (gold bar, topic in italic); Figtree for
everything else. Square corners. White background.

## Diagrams

- Canvas 1600 x 900. Header at the top left: title at 28 px, one-line takeaway at 18 px light;
  "Draft" tag top right.
- Box title 18 px semibold, sub-lines 15 px grey; arrow labels 14 px; step text 14 px.
- Legend on one line near the bottom; source line and "2026 / Strictly confidential" at the foot.
- Markers are circles r=15 with white bold letters, drawn last so no line crosses them.
- Arrow kinds: solid olive ink (data moves), grey dashed (keyed by a person), light grey dashed (runs
  alongside, fading out), olive dashed (redo or feedback loop).

## The page

- Paper header band: a label "Sunridge Partners · Internal · Draft", the h1 "Company | *Topic, Before
  and After*", a meta line (date · author · live since), and a lead that gives the headline numbers.
- Each section: an h2 under a 2 px olive rule, a "say" line that changes with the switch, the switch
  (Before / After, or up to four views), the figure in a frame that scrolls sideways on a phone.
- Tables: uppercase small headers, the After column on sage.
- Footer: where the figures come from and when; "Sunridge Partners – Confidential".
- Single light theme; it must read at 390 px wide with no sideways page scroll.
