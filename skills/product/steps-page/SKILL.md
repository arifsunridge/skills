---
name: steps-page
description: Build a clickable steps page (an Artifact) that walks a person with only a browser through steps only they can do, with "Send this to Claude" boxes where Claude acts or checks. Use when a deploy, go-live, setup or cutover needs someone else's clicks in Render, GitHub, Cloudflare, a portal admin screen or any dashboard, or when the user asks for a steps page, setup guide, checklist or "dashboard of steps". For a person with a terminal, the wizard skill fits better.
---

# Steps page

A **steps page** is a published Artifact that walks a person through a manual procedure in a browser: one numbered step at a time, each saying where to go (a button that opens the exact page), what to click and what to type, with a Copy button on every value. Ticks are remembered in their browser. Where Claude must act (deploy, re-run a check, read a log), the step holds a blue **hand-back** box: the exact message to paste into the chat.

The page engine is solved in [template.html](template.html): sticky progress bar, one open step at a time, Done / Skip / Undo, Copy buttons, light and dark themes, phone width. The library above and below the `PAGE` block is identical on every steps page; that sameness is the point, so people learn the page once. **Your job is to scope the procedure and write the `PAGE` block.**

## 1. Scope the procedure

List every action only the person can take: dashboards you have no access to, settings your tools are refused, approvals that are theirs. Read the repo and the services first, then ask only what you cannot look up:

- Config the deploy reads: `render.yaml`, `.env.example`, `.github/workflows/*`, docs on setup or deploy.
- The live state, through your tools where you have them: the service's branch and auto-deploy trigger, the repo's rulesets, which variables exist.
- What would break if steps ran out of order (a variable the live version would refuse, a token the build needs first).

Done when every step is something you checked that you cannot do yourself, and every value they type is named.

## 2. Order the steps

- Group by where the work happens: one `part` per site (GitHub, Render: service, Cloudflare, Portal). Within a part, the order the screens are reached.
- Put the **deploy gate** last: a step whose hand-back box says what is done and asks Claude to deploy. A step that must follow the deploy (a setting the old version would refuse) belongs to Claude after the gate; say so in a `warn` callout at the top.
- End with one **look-around** step: three things to try in the live app, and a hand-back box to report.
- Aim for 4 to 8 steps. A step with more than five actions is two steps.

## 3. Write the PAGE block

Copy `template.html` to the scratchpad, replace `__TITLE__` in the `<title>`, and fill `PAGE`:

- `key`: unique per page (`<project>-<job>-v1`); bump the version when the steps change, or old ticks hide new steps.
- `callouts`: the safety facts the person needs before starting: what cannot break, what to leave alone until later.
- Each step: `id`, `title` (the action, imperative), `sub` (the click path: `service → Settings → Auto-Deploy`), and `body` built from the helpers: `link(url, text)` for the exact page, `value(label, text)` for anything typed, `<ol class="do">` for the clicks, `note(html, kind)` for a warning inside a step, `claude(message)` for the hand-back.
- Deep links beat directions: link the exact settings page (`/web/<service-id>/env`, `/<owner>/<repo>/settings/rules`), not the dashboard home.
- Name buttons exactly as the screen does, in bold. Say which save button when there are two ("Save only, not Save, rebuild and deploy").
- Hand-back messages state facts Claude will verify ("Auto-Deploy is After CI Checks Pass"), so a skipped step shows up when Claude checks.
- Values carry names, ids and settings only. Secrets travel through the person's password manager or a one-time link; the page says where the secret comes from ("the same token you put on the other apps").

Recipes for steps that recur (Render variables and auto-deploy, GitHub rulesets and package access, Cloudflare Access, portal grants): [patterns.md](patterns.md).

## 4. Check and publish

Open the page once (the Artifact preview, or one Playwright run of the file): the step count is right, Done opens the next step, no console error. Publish with the Artifact tool, `icon: "checklist"`, and a one-sentence description naming the job.

In the reply, give the link and the one or two facts the person must know before starting. When they send a hand-back message, verify the facts it states with your own tools before acting on it.
