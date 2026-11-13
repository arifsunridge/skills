# Sunridge Skills

Agent skills for product and engineering work that has to survive contact with reality: alignment before build, evidence before claims, tight loops when something breaks, and time-boxed teams of subagents when the job is bigger than one context window.

Forked in spirit from [Matt Pocock's skills](https://github.com/mattpocock/skills): small, composable, editable. Adapted for Sunridge workflows where the deliverable is often a **value case**, a **go-live**, or a **research pack**, not only a PR.

## Install

```bash
npx skills@latest add arifsunridge/skills -a cursor
```

Or clone this repo and point your agent at `skills/`. Claude Code plugin layout lives in `.claude-plugin/plugin.json`.

## What's a skill?

A skill is a focused, repeatable workflow an agent can run. It is a small markdown file (plus any scripts or templates it needs) that writes down the exact moves you want every time: inputs, steps, completion criteria, and what "done" looks like.

These skills split on one axis: **who can invoke them**.

- **User-invoked** — you type them (e.g. `/grill-me`). Their job is to start a session on purpose.
- **Model-invoked** — you can type them, and the agent can also reach for them when the task fits. They hold the reusable discipline.

## Catalog

### Productivity

| Skill | Invoke | What it does |
| --- | --- | --- |
| **[grill-me](./skills/productivity/grill-me/SKILL.md)** | User | Relentless interview wrapper. Use when you want to start grilling on purpose. |
| **[grilling](./skills/productivity/grilling/SKILL.md)** | Model | Design-tree interview in rounds. Stress-tests plans, product calls, and go-lives until nothing important is assumed. |

Docs: [grilling](./docs/productivity/grilling.md) · [grill-me](./docs/productivity/grill-me.md)

### Engineering

| Skill | Invoke | What it does |
| --- | --- | --- |
| **[code-review](./skills/engineering/code-review/SKILL.md)** | Model | Three-axis review since a fixed point: **Standards**, **Spec**, and **Outcome** (did the user-visible result actually land?). |
| **[diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md)** | Model | Hard-bug discipline: tight red loop → minimise → hypothesise → instrument → fix → regression. Also for broken product flows. |
| **[research](./skills/engineering/research/SKILL.md)** | Model | Primary-source investigation into a cited Markdown brief (technical, product, comparative, or evidence pack). |

Docs: [code-review](./docs/engineering/code-review.md) · [diagnosing-bugs](./docs/engineering/diagnosing-bugs.md) · [research](./docs/engineering/research.md)

### Product artifacts

| Skill | Invoke | What it does |
| --- | --- | --- |
| **[value-case-flows](./skills/product/value-case-flows/SKILL.md)** | Model | Before/after data and process flows as a Sunridge-style interactive page (what changed, still manual, measures with sources). |
| **[steps-page](./skills/product/steps-page/SKILL.md)** | Model | Clickable browser checklist for steps only a human can do, with Copy buttons and "Send this to Claude" hand-backs. |

Docs: [value-case-flows](./docs/product/value-case-flows.md) · [steps-page](./docs/product/steps-page.md)

### Orchestration

| Skill | Invoke | What it does |
| --- | --- | --- |
| **[orchestrate](./skills/orchestrate/SKILL.md)** | Model | Time-boxed fan-out across subagents, each on the model that fits the job. Coding, audits, research, value cases, go-lives, stakeholder packs. |

Docs: [orchestrate](./docs/orchestrate/orchestrate.md)

## How they fit together

```text
  grill-me / grilling
        │
        ▼
   shared understanding
        │
        ├─► research ──────────────► evidence pack
        ├─► value-case-flows ──────► before/after page
        ├─► steps-page ────────────► human go-live checklist
        ├─► diagnosing-bugs ───────► tight red loop → fix
        ├─► code-review ───────────► Standards / Spec / Outcome
        └─► orchestrate ───────────► time-boxed team of the above
```

Typical paths:

1. **Align then ship** — `/grill-me` → build → `/code-review`.
2. **Portco value case** — `/grill-me` → `/research` (evidence) → `/value-case-flows`.
3. **Go-live** — `/grill-me` → `/steps-page` → hand-backs verified in chat.
4. **Something's broken** — `/diagnosing-bugs` (do not hypothesise before a red loop).
5. **Too big for one agent** — `/orchestrate` with a deadline; it fans into the skills above.

## What changed vs Matt Pocock

| Area | Matt | Sunridge |
| --- | --- | --- |
| Grilling | Plan / design focus | Same rounds + frontier; also product calls, go-lives, manual residue, next-artifact handoff |
| Review | Standards + Spec | Adds **Outcome** axis (acceptance / value-case After / go-live result) |
| Diagnosis | Code + perf | Same phases; adds product/ops red loops and steps-page HITL |
| Research | Repo notes from primary sources | Same, plus product/vendor/comparative/evidence-pack branches |
| Artifacts | Wizard (terminal) | **steps-page** (browser) and **value-case-flows** (Sunridge flows page) |
| Fan-out | Implement-spec / chief-of-staff (code-heavy) | **orchestrate**: time box + model fit for product _and_ engineering work |

## Detailed skill pages

Each skill has a short human doc under `docs/` covering when to reach for it, how it works, and what "it's working" looks like. The agent-facing source of truth remains each `SKILL.md`.
