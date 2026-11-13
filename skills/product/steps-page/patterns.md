# Step recipes

Bodies for steps that recur across projects. Copy one into a step's `body`, change the names and links, and keep the shape. Each was used on a real go-live; the screen names match Render, GitHub and Cloudflare as of October 2026, so check a screen against the live site when a person reports a missing button.

## Render: add an environment variable

```js
{ id: 'npm', title: 'The package token', sub: 'my-service → Environment', body: () => `
  <p class="why">The build installs a private package and needs this token.</p>
  <div class="links">${link(SERVICE + '/env', 'Open my-service Environment')}</div>
  <ol class="do"><li>If <code>NPM_TOKEN</code> is already there, press <b>Done</b>.</li>
  <li>Otherwise <b>Add Environment Variable</b>: the key below, the value from your password manager.</li>
  <li>Click <b>Save only</b>, not “Save, rebuild and deploy”.</li></ol>
  ${value('Key', 'NPM_TOKEN')}` },
```

`SERVICE` is `https://dashboard.render.com/web/<service-id>`. "Save only" keeps today's version live; the deploy gate deploys.

A variable the live version would refuse (a new value of an old setting) is not a person's step: Claude sets it after the deploy, and a `warn` callout says so.

## Render: deploy only after the tests pass

```js
{ id: 'auto', title: 'Deploy only after the tests pass', sub: 'my-service → Settings → Auto-Deploy', body: () => `
  <p class="why">Today the service deploys every commit at once.</p>
  <div class="links">${link(SERVICE + '/settings', 'Open my-service Settings')}</div>
  <ol class="do"><li>Under <b>Build &amp; Deploy</b>, find <b>Auto-Deploy</b> and click <b>Edit</b>.</li>
  <li>Choose <b>After CI Checks Pass</b> and save.</li></ol>` },
```

Verify afterwards: the service's `autoDeployTrigger` reads `checksPass`.

## GitHub: protect the branch Render deploys

```js
{ id: 'ruleset', title: 'Protect the live branch', sub: 'my-repo → Settings → Rules → Rulesets', body: () => `
  <div class="links">${link(REPO + '/settings/rules', 'Open my-repo rulesets')}</div>
  <ol class="do">
    <li><b>New ruleset</b> → <b>New branch ruleset</b>. Name: <code>live branch</code>. <b>Enforcement status</b>: <b>Active</b>.</li>
    <li><b>Target branches</b> → <b>Add target</b> → <b>Include default branch</b>.</li>
    <li>Leave <b>Restrict deletions</b> and <b>Block force pushes</b> ticked.</li>
    <li>Tick <b>Require status checks to pass</b>, <b>Add checks</b>, type <code>test</code> and pick it.</li>
    <li>Leave the bypass list empty. Click <b>Create</b>.</li>
  </ol>` },
```

When the live branch is not the default branch, use **Include by pattern** with the branch name in a `value()`, and a `warn` note saying so. The check name is the CI job's name; it appears in **Add checks** only after the workflow has run once on that repo. Verify afterwards with the rulesets API: `deletion`, `non_fast_forward`, `required_status_checks` with that context.

## GitHub: let a repo read a private package

```js
{ id: 'pkg', title: 'Let my-repo read the package', sub: 'Organization → Packages → my-package → Package settings', body: () => `
  <p class="why">CI installs the package with the run's own token, which GitHub refuses until the package lists this repo.</p>
  <div class="links">${link('https://github.com/orgs/MY-ORG/packages', 'Open MY-ORG packages')}</div>
  <ol class="do"><li>Click <b>my-package</b>, then <b>Package settings</b>.</li>
  <li>Under <b>Manage Actions access</b>, <b>Add Repository</b>, pick <code>my-repo</code>, role <b>Read</b>.</li></ol>
  ${claude('Package access is done for my-repo. Re-run its CI.')}` },
```

The symptom it fixes: `npm ci` fails with `403 ... permission_denied: read_package`.

## Cloudflare Access: protect a new address

```js
{ id: 'access', title: 'Put the address behind Cloudflare Access', sub: 'Zero Trust → Access → Applications', body: () => `
  <div class="links">${link('https://one.dash.cloudflare.com', 'Open Cloudflare Zero Trust')}</div>
  <ol class="do"><li><b>Add an application</b> → <b>Self-hosted</b>. Domain: the address below.</li>
  <li>Policies: the same as the other apps.</li>
  <li>Save, then copy the <b>Application Audience (AUD) Tag</b> into the service's <code>CF_ACCESS_AUD</code>.</li></ol>
  ${value('Address', 'my-app.example.com')}` },
```

## The deploy gate and the look-around

```js
{ id: 'deploy', title: 'Say “deploy my-app”', sub: 'Claude checks your settings, puts the tested work live', body: () => `
  ${claude('my-app steps are done: <each fact, as checked>. Deploy my-app.')}
  <div class="links">${link(SERVICE + '/events', 'Watch my-service Events')}</div>` },
{ id: 'try', title: 'Open the app and look around', sub: 'From the portal', body: () => `
  <div class="links">${link('https://my-app.example.com', 'Open my-app')}</div>
  <ol class="do"><li>One thing that proves sign-in works.</li><li>One thing that proves saving works.</li><li>One thing this change touched.</li></ol>
  ${claude('my-app is live and I looked around: [all fine / what I saw].')}` },
```

On "deploy": verify each stated fact with your tools (service settings, rulesets, CI green on the commit), then deploy, then read the start log before reporting.
