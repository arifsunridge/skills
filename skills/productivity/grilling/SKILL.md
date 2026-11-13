---
name: grilling
description: Grill the user relentlessly about a plan, decision, product call, or go-live. Use when the user wants to stress-test their thinking, align before building or shipping, or uses any grill trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work for product, ops, and engineering alike: a value case, a go-live, a process change, a PRD, or a technical design. Same mechanism. Different subject.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

## What to pressure

Bias recommendations toward things that survive contact with reality:

- **Owner**: who decides, who does, who signs off.
- **Evidence**: what number, log, screen, or source would prove the claim.
- **Failure**: what breaks if the decision is wrong, and how you would notice.
- **Manual residue**: what stays by hand after the change (name it; do not hide it).
- **Handoff**: whether the next artifact is a steps page, a value-case flows page, a research brief, tickets, or an orchestrated fan-out.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, live services), dispatch a sub-agent with a fresh context window to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

After confirmation, name the natural next skill once (steps-page, value-case-flows, research, code-review, diagnosing-bugs, or orchestrate) and wait; do not start it unasked.
