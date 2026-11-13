---
name: orchestrate
description: Run a large piece of work as a team of subagents, each on the model that fits its job, inside a time box. Use for whole-codebase reviews, audits, broad research, multi-part builds, value cases, go-lives, or multi-stakeholder packs when the user asks to "use subagents", "fan out", "orchestrate", or gives a deadline ("finish in 40 minutes").
---

# Orchestrate

You are the **conductor**, not a worker. Protect your context window. Almost all reading and producing happens in subagents with fresh context. You plan the cut, assign models, enforce the time box, and integrate.

This is not a coding-only skill. The same pattern covers engineering, product, research, and ops:

| Shape of work | Typical fan-out |
| --- | --- |
| Whole-codebase review / audit | One agent per area (security, standards, tests, UX, ops) |
| Broad research | One agent per question or source family |
| Multi-part build | One agent per independent slice on the ready frontier |
| Value case | Brief / evidence / diagram / page-check as parallel or staged agents |
| Go-live / cutover | Steps-page authoring + live-state checks + hand-back verification |
| Multi-stakeholder pack | One agent per audience artifact (board, eng, ops) sharing one evidence base |

## 1. Pin the time box and the outcome

Before spawning anyone:

1. **Time box.** If the user gave a deadline ("40 minutes", "by EOD"), use it. If not, propose one and get a yes. Work backwards from the deadline; do not discover the schedule after agents are running.
2. **Single outcome sentence.** What exists when the box ends (a report, a PR, a flows page, a steps page, a research pack). If you cannot say it in one sentence, grill first or cut scope.
3. **Done bar.** Three to five checkable criteria. Prefer artifacts and verified facts over "explored" or "understood".

## 2. Cut the work into jobs

Split into jobs that are:

- **Independent enough** to run without waiting on each other's full context.
- **Sized** to finish inside the remaining box (including your integrate step).
- **Owned by one skill** when a skill already exists: `research`, `code-review`, `diagnosing-bugs`, `grilling` (decisions stay with you / the user), `steps-page`, `value-case-flows`.

Write a one-screen **roster** before launch:

| Job | Deliverable | Skill / brief | Model fit | Depends on |
| --- | --- | --- | --- | --- |
| … | … | … | cheap / mid / strong | — or job id |

**Model fit** (pick what the harness allows; say the choice in the roster):

- **Strong**: synthesis, architecture judgement, grilling recommendations, final integrate.
- **Mid**: ordinary implementation, structured review axes, diagram/page assembly.
- **Cheap / fast**: mechanical scans, link checks, citation gathering, screenshot passes.

Never give two jobs the same write surface (same file, same PR body, same page section) unless they are strictly sequential.

## 3. Launch the wave

- Start every subagent with a **fresh context window**.
- Pass **context pointers** (paths, URLs, commit SHAs, ticket ids), not pasted novels.
- Tell each agent: its outcome, its done bar, its time budget, and what not to do (no drive-by refactors, no expanding scope).
- Prefer **background** agents so you can keep talking to the user and watch the clock.
- Run the **ready frontier** in parallel. A job whose inputs are not ready waits; do not fake independence.

If a job is a known skill, the subagent brief is: read that `SKILL.md` and execute it for this slice.

## 4. Steer inside the box

On a rough cadence of every quarter of the time box (or when an agent returns):

1. Mark jobs **done / blocked / drifting**.
2. **Cut or merge** jobs if the box is at risk; say what you dropped.
3. Unblock with a fact lookup or a single user question; do not open a full grilling round mid-fan-out unless decisions are truly stuck.
4. Keep a running **integrate draft** (headings only until results land).

When the box is nearly over, **stop launching**. Integrate what you have. Partial, honest output beats a late perfect plan.

## 5. Integrate and hand back

Produce one artifact the user can use:

- A single report with sections per job, or
- Links to the pages / PRs / files each job produced, plus your synthesis.

For each job state **kept**, **dropped**, or **follow-up**. Cite pointers. Do not re-ask the user to re-read every subagent transcript.

If the natural sequel is another skill (steps-page publish, value-case sign-off, code-review on the branch), name it once and wait.

## Rules

- You may dig yourself only to unblock integration or to verify a conflict between agents.
- Facts from the environment are your job to fetch (via subagents); decisions stay with the user.
- Redact secrets in every hand-off.
- Time box wins over completeness. Say what did not fit.
