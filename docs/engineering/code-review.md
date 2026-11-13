## What it does

Reviews the diff since a fixed point on three axes, each in its own sub-agent:

1. **Standards** — repo coding standards + Fowler smell baseline
2. **Spec** — originating ticket / spec fidelity
3. **Outcome** — whether the claimed user or operational result actually landed

## When to reach for it

Branch reviews, PR reviews, "review since main", or before you call a change done.

## How it differs here

Matt's skill uses Standards + Spec. Sunridge adds **Outcome** so a change can pass the ticket text and still fail the value-case After state or acceptance criteria.

## It's working if

- Axes are reported separately, not merged into one ranked list.
- Missing spec or outcome sources are skipped explicitly, not invented.
- Smell findings stay judgement calls unless a documented standard hardens them.
