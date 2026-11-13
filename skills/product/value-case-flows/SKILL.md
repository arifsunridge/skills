---
name: value-case-flows
description: Model how an app or process change works before and after, and publish it as a Sunridge-style interactive flows page (data flow, process swimlane, deep-dive flows, what changed, still manual). Use when asked to show or explain a before/after, draw data or process flows, build a flows page, or make a value case for a portco app.
---

# Value-case flows

Turn "how did this work before, and how does it work now" into one interactive page in Sunridge House
Style: a data flow and a process swimlane, each with a Before/After switch, optional deep-dive flows,
a key for the markers, a What changed table and a Still manual table. Worked examples: HBF Planning
Flows (https://claude.ai/artifact/Ldwy1sssS45ufdYtM22YFf) and HBF Costing Flows
(https://claude.ai/artifact/5cGYRgTkiYMgxenUQqCcGK).

Scripts live in `scripts/` next to this file; run them with `python3` from a working folder of your own.

## Steps

1. **Write the brief** from `references/brief-template.md` into the working folder: audience, the
   app and its live date, the lanes, the numbered Before and After steps, the still-open items, the
   measures with their source and date, and the effort table. Done when every step has an owner and
   every number has a source, a date and a legend tag (Recorded, Measured, Estimate).
2. **Trace it from evidence.** Read the code, the docs and live read-only data for every claim in the
   brief; ask the person for what only they know (the old way, the meetings). Record each correction
   in the brief. Done when no line rests on memory or on an earlier draft.
3. **Model** with `references/modeling.md`: pick the diagram kinds, the lanes, the markers and the
   rows of each table. Done when every marker on a Before diagram has its After state and its Key line.
4. **Draw.** Copy `scripts/svgkit.py`, `scripts/example_dataflow.py` and `scripts/example_process.py`
   into the working folder, keep the examples' shape, replace boxes, arrows, steps and markers with the
   brief's; `svgkit.py` holds the primitives and `references/house-style.md` the rules. Run each
   into `out/`. Done when `report()` prints no OVERFLOW (step 6's images catch the rest).
5. **Build the page.** Copy `assets/example-spec.json` to `spec.json` next to `out/`, fill it from the
   brief, then `python3 scripts/build_flows_page.py spec.json page.html`.
6. **Check.** `python3 scripts/check_page.py page.html --shots shots/` (add `--no-money` when the
   company's rule is counts only). Look at every image in `shots/` (both page widths and each diagram
   view), and fix any line through a label or box back in step 4. Done when it prints OK (or every
   money hit is a tolerance or rule, not a price) and every image is clean.
7. **Publish** `page.html` as an HTML artifact (the Artifact tool in Claude Code; an HTML artifact in a
   chat). Title it "<Company> <Topic> Flows". Hand over the offline copy too, and say who can open the
   link (private until shared).

## Rules

- Counts, shares and dates; money only where the company allows it, and never in an example.
- Every number names its source and date; every effort figure says "~" and "estimate".
- The After shows what is still by hand, honestly: keyed by a person, runs alongside, not live yet.
- Plain, direct writing in the person's words for things (their system and role names); no em dashes.
- Diagrams and pages carry "Draft" until the owner signs them off.
