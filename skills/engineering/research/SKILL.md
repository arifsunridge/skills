---
name: research
description: Investigate a question against high-trust primary sources and capture cited findings. Use when the user wants a topic researched, docs or API facts gathered, product/vendor/market reading, or reading legwork delegated to a background agent.
---

Spin up a **background agent** to do the research, so you keep working while it reads. Start it with a fresh context window.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs, vendor docs, filings, raw datasets), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source with a link or path and the date you read it.
3. Save it where the work already keeps such notes:
   - Code / API facts → match the repo's convention; if none, put it somewhere sensible and say where.
   - Product, vendor, market, or ops briefs → prefer `docs/research/` or a path the user names.
4. Open with a 3–5 line **verdict**, then the evidence. Separate **known**, **unknown**, and **needs a decision**.

## Scope branches

Name which branch you are on in the brief you give the sub-agent:

- **Technical**: how a library, API, or codebase behaves.
- **Product / process**: how a workflow works today, what a vendor claims, what a portco app does.
- **Comparative**: two or more options against the same criteria; table the criteria, do not crown a winner unless the user asked for a recommendation.
- **Evidence pack**: gather sources for a later value-case flows page or grilling session; stop at facts, leave decisions to the user.

## Rules

- Prefer primary sources. When only a secondary source exists, label it as secondary and say what primary source would supersede it.
- Never invent citations. If you cannot find it, put it under **unknown**.
- Redact secrets in quoted material.
- If the question is too large for one pass, say so and either (a) propose a slice the background agent can finish, or (b) hand the fan-out to **orchestrate** with one research agent per slice.
