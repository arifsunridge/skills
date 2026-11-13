# Modeling a before and after

## The kinds of diagram

| Kind | Shows | Build it so |
|---|---|---|
| Data flow | Where data moves between people, systems and the app, and where it breaks | One geometry for Before and After: the same boxes in the same places, so flipping the switch shows only what changed. People and parties white, systems paper, the app sage. A side panel: "Where it breaks" before, "What changed" after. |
| Process swimlane | How one unit (a Job, an order, a cost card) gets done, step by step | One lane per role or system, the app lane greyed in the Before. Steps numbered as in the brief; decisions as diamonds; what lands in a system as a chip; the redo loop dashed. Steps the app does are sage. |
| Deep-dive flow | One mechanism inside the app (how a price is set, how a version is signed) | Only when the audience needs to check the rules. One diagram per mechanism, each with its rule, its owner and where it lives in the code, in a 3 to 4 way switch section with a rule line under it. |

Two sections (Data flow, Process) is the default page; add the deep-dive section for an internal
audience.

## Markers

A marker is a lettered circle placed where the old way loses something. Define the letters per case
and list each in the Key; these four covered both HBF packs:

| Letter | Means | Before | After |
|---|---|---|---|
| R | Retyped by hand (R1, R2... in step order) | RED | GREY when a person still keys it by design; gone when the app removes it |
| D | A date lost (in an inbox, in memory, left blank) | GOLD | GREEN: kept as a dated event with a reason |
| G | A number guessed or back-solved | RED | gone: comes from a source |
| T | A term read from free text | RED | gone: structured |

The same marker sits at the same place on the data flow and the process, so the reader can follow it.

## Effort table

By role, hours a week, before and after. Each row shows its arithmetic in words: count x minutes
("~10 a week, 15 min to 1 min"). Total the column. Label every figure "~" and "estimate" and ask each
owner to correct their row; the page shows the totals only.

## What changed table

Rows are the measures a manager asks about: times typed by hand, hand-offs, effort, freshness of the
data, share of records complete, whether a reason is kept. Before in plain text, After on sage, with
"(estimate ...)" after any estimate. Use the measured share where one exists ("293 of 328 open Jobs").

## Still manual table

Gap, what removes it, owner. The gaps are what the After diagram draws grey or dashed: keyed by a
person, runs alongside, not live yet, waiting to deploy.

## Pitfalls seen

- A delay or a mechanism stated from memory is often wrong: one pack said "about an hour behind"
  where the read was overnight extracts; another said "lot-traced" where the card priced from PO
  receipts. Check each against the code or a live read before it goes on a diagram.
- An agent's summary of code can invent behaviour (a stale line counted as supply when the code
  leaves it out). Read the code line it cites.
- Before and After drawn with different layouts look like two stories; keep one geometry.
- A label placed on a line, or a line through a box, makes the page look careless: look at every
  rendered diagram, not just the overflow report.
