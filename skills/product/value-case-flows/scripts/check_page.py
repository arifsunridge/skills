"""check_page: prove a flows page is ready to publish.

  python3 check_page.py page.html [--no-money] [--shots DIR]

With --shots, DIR gets page-1280.png and page-390.png (whole page) and <section>-<view>.png (each
diagram view at 1280 px), so every view can be looked at.

Static checks (always): no duplicate ids; every switch button has its figure; with --no-money, no
currency amount anywhere (a "$" followed by a digit). Browser checks (when Python Playwright is
installed): at 1280 px and 390 px the page loads with no script error, every switch view shows,
and the page never scrolls sideways (figures scroll inside their own frame). Set CHROME to a
browser binary if Playwright has no browser of its own. Exits 1 on any failure.
"""
import os
import pathlib
import re
import sys


def static(text, no_money):
    bad = []
    ids = re.findall(r'\bid="([^"]+)"', text)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        bad.append(f"duplicate ids: {dup[:8]}")
    for sec, view in re.findall(r'data-sec="([^"]+)" data-view="([^"]+)"', text):
        if f'id="{sec}-{view}"' not in text:
            bad.append(f"button {sec}/{view} has no figure #{sec}-{view}")
    if no_money:
        hits = re.findall(r"[^\s<>]{0,30}\$\s?\d[^<]{0,30}", text)
        if hits:
            bad.append(f"currency amounts: {hits[:5]}")
    return bad


def browser(path, shots):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("browser checks skipped: Python Playwright not installed (pip install playwright)")
        return []
    bad = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROME") or None)
        for width in (1280, 390):
            pg = b.new_page(viewport={"width": width, "height": 900})
            errors = []
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.goto(pathlib.Path(path).resolve().as_uri())
            pg.wait_for_timeout(300)
            over = pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            if over > 0:
                wide = pg.evaluate("""[...document.querySelectorAll('body *')].filter(e => !e.closest('svg') &&
                    e.getBoundingClientRect().right > window.innerWidth + 1).slice(0, 3)
                    .map(e => e.tagName + '.' + e.className + '#' + e.id).join(', ')""")
                bad.append(f"{width} px: page scrolls sideways by {over} px ({wide})")
            for btn in pg.query_selector_all(".switch button"):
                sec, view = btn.get_attribute("data-sec"), btn.get_attribute("data-view")
                btn.click()
                if pg.evaluate(f"document.getElementById('{sec}-{view}').hidden"):
                    bad.append(f"{width} px: view {sec}/{view} did not show")
                elif shots and width == 1280:
                    os.makedirs(shots, exist_ok=True)
                    pg.query_selector(f"#{sec}-{view} svg").screenshot(path=os.path.join(shots, f"{sec}-{view}.png"))
            bad += [f"{width} px: script error {e}" for e in errors]
            if shots:
                os.makedirs(shots, exist_ok=True)
                pg.screenshot(path=os.path.join(shots, f"page-{width}.png"), full_page=True)
            pg.close()
        b.close()
    return bad


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    shots = args[args.index("--shots") + 1] if "--shots" in args else None
    page = args[0]
    problems = static(pathlib.Path(page).read_text(), "--no-money" in args) + browser(page, shots)
    for p in problems:
        print("FAIL", p)
    print("OK" if not problems else f"{len(problems)} problem(s)")
    sys.exit(1 if problems else 0)
