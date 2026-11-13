## What it does

Forces a **tight red loop** before any hypothesis. Then: minimise → hypothesise → instrument → fix → regression → cleanup.

## When to reach for it

"It's broken", "debug this", flaky failures, slow paths, or a product flow that used to work.

## How it differs here

Same spine as Matt's skill. Sunridge adds **product/ops red** loops (assert the user-visible symptom) and points HITL toward a **steps-page** when the human only has a browser.

## It's working if

- You see a command that already went red on the user's exact symptom before theories appear.
- Hypotheses are falsifiable and ranked.
- Debug tags are cleaned up before "done".
