"""build_flows_page: turn a JSON spec plus SVG diagrams into one self-contained flows page.

  python3 build_flows_page.py spec.json page.html

The page: a paper header band, then one section per entry in `sections` (each a switch over 2 to 4
SVG views, with a one-line "say" and an optional "rule" per view), then the optional key, "What
changed" and "Still manual" blocks, then the footer. SVG paths in the spec are relative to the spec
file. Each SVG's ids are prefixed per view so markers and titles stay unique on one page. Links like
page.html#data-after open a view directly. See assets/example-spec.json for every field.
"""
import html
import json
import pathlib
import re
import sys

CSS = """/* Sunridge House Style, single light theme ("Print and screen"): paper header band, white content, square corners, gold only as accent. */
:root {
  --paper: #F7F5F0; --white: #FFFFFF; --ink: #2D2D2D; --olive-ink: #535349; --olive: #61664E;
  --gold: #D8A45F; --gold-dark: #B8853F; --sage-light: #DDE5DC; --grey: #6F6F6F; --grey-light: #CCCCCC; --grey-line: #EEEEEE;
  --rag-red: #B5543C; --rag-green: #7D8F5E;
  --display: 'Libre Baskerville', Georgia, 'Times New Roman', serif;
  --body: Figtree, system-ui, 'Segoe UI', sans-serif;
  color-scheme: light;
}
* { box-sizing: border-box; }
body { background: var(--white); color: var(--ink); font-family: var(--body); font-size: 15px; line-height: 1.5; font-weight: 400; }
.wrap { max-width: 1200px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
header.band { background: var(--paper); border-bottom: 1px solid var(--grey-light); }
header .wrap { padding-block: 28px 32px; display: grid; gap: 14px; }
.label { font-size: 12px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: var(--grey); }
h1 { font-family: var(--display); font-weight: 400; font-size: clamp(24px, 3.4vw, 34px); line-height: 1.25; color: var(--olive-ink); margin: 0; text-wrap: balance; }
h1 .bar, h2 .bar { color: var(--gold); }
h1 em, h2 em { font-style: italic; }
.meta { color: var(--grey); font-size: 14px; }
.lead { font-size: 18px; font-weight: 300; max-width: 68ch; margin: 0; }
.lead strong { font-weight: 600; }
main .wrap { padding-block: 8px 48px; display: grid; gap: 48px; }
section { display: grid; gap: 16px; min-width: 0; }
h2 { font-family: var(--display); font-weight: 400; font-size: 22px; line-height: 1.3; color: var(--olive-ink); margin: 0; padding-top: 28px; border-top: 2px solid var(--olive); text-wrap: balance; }
.sec-head { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px 24px; }
.sec-head p { margin: 0; max-width: 72ch; font-weight: 300; font-size: 16px; min-width: 0; flex: 1 1 420px; }
.sec-head p strong { font-weight: 600; }
.switch { display: inline-flex; border: 1px solid var(--olive); border-radius: 4px; overflow: hidden; flex: none; }
.switch button { font: 600 13px/1 var(--body); letter-spacing: .5px; padding: 10px 18px; background: var(--white); color: var(--olive-ink); border: 0; cursor: pointer; }
.switch button + button { border-left: 1px solid var(--olive); }
.switch button[aria-pressed="true"] { background: var(--olive-ink); color: var(--white); }
.switch button:hover:not([aria-pressed="true"]) { background: var(--sage-light); }
.switch button:focus-visible { outline: 2px solid var(--gold-dark); outline-offset: -4px; }
.figure { border: 1px solid var(--grey-light); background: var(--white); overflow-x: auto; }
.figure svg { display: block; width: 100%; min-width: 880px; height: auto; }
.hint { font-size: 12px; color: var(--grey); margin: 0; }
@media (min-width: 900px) { .hint { display: none; } }
table { border-collapse: collapse; width: 100%; font-size: 15px; font-variant-numeric: tabular-nums; }
.tbl { overflow-x: auto; }
th { text-align: left; font-size: 12px; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; color: var(--olive-ink); padding: 10px 14px 8px 0; border-bottom: 2px solid var(--olive); }
td { padding: 11px 14px 11px 0; border-bottom: 1px solid var(--grey-line); vertical-align: top; }
td:first-child { font-weight: 600; color: var(--olive-ink); width: 26%; }
td.before { color: var(--ink); }
td.after { background: var(--sage-light); padding-left: 12px; }
th.after-h { padding-left: 12px; }
.est { color: var(--grey); font-size: 13px; }
.key { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px 32px; }
.key div { min-width: 0; }
.key h3 { margin: 0 0 6px; font-size: 12px; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; color: var(--olive-ink); }
.key ul { margin: 0; padding: 0; list-style: none; display: grid; gap: 6px; }
.key li { display: grid; grid-template-columns: 34px 1fr; gap: 8px; align-items: baseline; }
.code { font-weight: 600; font-size: 13px; color: var(--white); background: var(--grey); text-align: center; padding: 2px 0; }
.code.d { background: var(--rag-red); }
.code.d.kept { background: var(--rag-green); }
footer { border-top: 1px solid var(--grey-line); }
footer .wrap { padding-block: 16px 28px; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px 24px; font-size: 12px; color: var(--grey); }
@media (prefers-reduced-motion: no-preference) { .figure svg { animation: fade .25s ease-out; } @keyframes fade { from { opacity: .35; } to { opacity: 1; } } }
.switch.four button { padding: 10px 14px; }
@media (max-width: 480px) { .switch.four button { padding: 10px 7px; letter-spacing: 0; } }
.rule { margin: 0; font-size: 14px; color: var(--grey); max-width: 90ch; }
.code.g { background: var(--gold); }
.code.k { background: var(--grey); }"""

SCRIPT = """(function () {
  var V = %s;
  function show(sec, view) {
    V[sec].views.forEach(function (v) {
      document.getElementById(sec + '-' + v).hidden = (v !== view);
      document.getElementById(sec + '-btn-' + v).setAttribute('aria-pressed', String(v === view));
    });
    document.getElementById(sec + '-say').innerHTML = V[sec].say[view];
    var r = document.getElementById(sec + '-rule');
    if (r) r.textContent = V[sec].rule[view] || '';
  }
  document.querySelectorAll('.switch button').forEach(function (b) {
    b.addEventListener('click', function () { show(b.dataset.sec, b.dataset.view); });
  });
  Object.keys(V).forEach(function (s) { show(s, V[s].views[0]); });
  var m = /^([a-z0-9]+)-([a-z0-9]+)$/.exec((location.hash || '').slice(1));
  if (m && V[m[1]] && V[m[1]].views.indexOf(m[2]) >= 0) show(m[1], m[2]);
})();"""


def inline_svg(path, prefix):
    """The SVG's markup with every id, url(#id) and aria-labelledby prefixed; fixed size dropped."""
    s = pathlib.Path(path).read_text().strip()
    s = re.sub(r"^<\?xml[^>]*>\s*", "", s)
    for i in sorted(set(re.findall(r'\bid="([^"]+)"', s)), key=len, reverse=True):
        s = re.sub(rf'\bid="{re.escape(i)}"', f'id="{prefix}-{i}"', s)
        s = s.replace(f"url(#{i})", f"url(#{prefix}-{i})")
    s = re.sub(r'aria-labelledby="([^"]*)"',
               lambda m: 'aria-labelledby="' + " ".join(f"{prefix}-{x}" for x in m.group(1).split()) + '"', s)
    return re.sub(r'(<svg[^>]*?)\s(?:width|height)="\d+"\s(?:width|height)="\d+"', r"\1", s, count=1)


def heading(level, pair, hid=None):
    """'Section | *Topic*' with the gold bar."""
    first, topic = pair
    attr = f' id="{hid}"' if hid else ""
    return f'<h{level}{attr}>{html.escape(first)} <span class="bar">|</span> <em>{html.escape(topic)}</em></h{level}>'


def section(sec, base, js):
    sid, views = sec["id"], sec["views"]
    keys = [sid] + [v["key"] for v in views]
    if not all(re.fullmatch(r"[a-z0-9]+", k) for k in keys) or not 2 <= len(views) <= 4:
        sys.exit(f"section {sid}: the id and view keys must be lowercase letters/digits, with 2 to 4 views")
    four = " four" if len(views) > 2 else ""
    btns = "".join(f'<button type="button" id="{sid}-btn-{v["key"]}" data-sec="{sid}" data-view="{v["key"]}" '
                   f'aria-pressed="{str(i == 0).lower()}">{html.escape(v["label"])}</button>'
                   for i, v in enumerate(views))
    figs = "".join(f'<div class="figure" id="{sid}-{v["key"]}"{"" if i == 0 else " hidden"}>'
                   f'{inline_svg(base / v["svg"], sid + v["key"])}</div>\n' for i, v in enumerate(views))
    has_rule = any(v.get("rule") for v in views)
    js[sid] = {"views": [v["key"] for v in views], "say": {v["key"]: v["say"] for v in views},
               "rule": {v["key"]: v.get("rule", "") for v in views}}
    return f"""    <section aria-labelledby="h-{sid}">
      {heading(2, sec["h2"], "h-" + sid)}
      <div class="sec-head">
        <p id="{sid}-say"></p>
        <div class="switch{four}" role="group" aria-label="{html.escape(sec["h2"][0])} view">{btns}</div>
      </div>
      {figs}{f'<p class="rule" id="{sid}-rule"></p>' if has_rule else ""}
      <p class="hint">Scroll sideways to see the whole diagram.</p>
    </section>
"""


def key_block(groups):
    cols = ""
    for g in groups:
        items = "".join(f'<li><span class="code {it.get("tone", "d")}">{html.escape(it["code"])}</span>'
                        f'<span>{html.escape(it["text"])}</span></li>' for it in g["items"])
        cols += f'<div><h3>{html.escape(g["title"])}</h3><ul>{items}</ul></div>'
    return f"""    <section aria-labelledby="h-key">
      {heading(2, ["Key", "the codes on the diagrams"], "h-key")}
      <div class="key">{cols}</div>
    </section>
"""


def table_block(sid, t, after_col):
    after_h = ' class="after-h"'
    head = "".join(f'<th scope="col"{after_h if after_col and i == 2 else ""}>{html.escape(h)}</th>'
                   for i, h in enumerate(t["head"]))
    rows = ""
    for r in t["rows"]:
        cells = ""
        for i, c in enumerate(r[:len(t["head"])]):
            cls = ' class="after"' if after_col and i == 2 else (' class="before"' if after_col and i == 1 else "")
            cells += f"<td{cls}>{html.escape(c)}"
            if after_col and i == 2 and len(r) > 3 and r[3]:
                cells += f' <span class="est">({html.escape(r[3])})</span>'
            cells += "</td>"
        rows += f"<tr>{cells}</tr>"
    return f"""    <section aria-labelledby="h-{sid}">
      {heading(2, t["h2"], "h-" + sid)}
      <div class="tbl"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>
    </section>
"""


def build(spec_path, out_path):
    spec_path = pathlib.Path(spec_path)
    spec, base, js = json.loads(spec_path.read_text()), spec_path.parent, {}
    body = "".join(section(s, base, js) for s in spec["sections"])
    if spec.get("key"):
        body += key_block(spec["key"])
    if spec.get("changed"):
        body += table_block("change", spec["changed"], after_col=True)
    if spec.get("gaps"):
        body += table_block("gap", spec["gaps"], after_col=False)
    h = spec["header"]
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(spec["title"])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:ital,wght@0,300;0,400;0,600;1,300&family=Libre+Baskerville:ital,wght@0,400;1,400&display=swap">
<style>
body {{ margin: 0; }}
{CSS}
</style>
</head>
<body>
<header class="band">
  <div class="wrap">
    <div class="label">{html.escape(h["label"])}</div>
    {heading(1, h["h1"])}
    <div class="meta">{html.escape(h["meta"])}</div>
    <p class="lead">{h["lead_html"]}</p>
  </div>
</header>
<main>
  <div class="wrap">
{body}  </div>
</main>
<footer>
  <div class="wrap">
    <span>{html.escape(spec["footer"][0])}</span>
    <span>{html.escape(spec["footer"][1])}</span>
  </div>
</footer>
<script>
{SCRIPT % json.dumps(js, ensure_ascii=False)}
</script>
</body>
</html>
"""
    pathlib.Path(out_path).write_text(page)
    print(f"wrote {out_path} ({len(page) // 1024} KB, {len(spec['sections'])} sections)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    build(sys.argv[1], sys.argv[2])
