"""svgkit: a small SVG builder for Sunridge House Style flow diagrams (1600 px wide canvas).

Draw with the primitives (rect, text, path, badge, stepnum, diamond), the page furniture (header,
footer, legend) and the layout helpers (box, lanes, step, chip, panel). Text is measured with an
embedded Figtree width table, so `check` flags any line wider than its box with no font files needed.
Call `report()` at the end of a generator: it prints every overflow and exits 1 if there was one.
"""
import json
import sys
from xml.sax.saxutils import escape

# Figtree advance widths per character at 1000 units, weights 300/400/600/700 (measured from the TTFs).
_METRICS = json.loads(r"""{"300": {" ": 250, "!": 292, "\"": 284, "#": 628, "$": 567, "%": 775, "&": 642, "'": 182, "(": 340, ")": 340, "*": 478, "+": 620, ",": 214, "-": 420, ".": 192, "/": 372, "0": 638, "1": 410, "2": 551, "3": 539, "4": 616, "5": 572, "6": 560, "7": 530, "8": 615, "9": 560, ":": 234, ";": 241, "<": 620, "=": 620, ">": 620, "?": 500, "@": 988, "A": 662, "B": 610, "C": 719, "D": 683, "E": 593, "F": 539, "G": 767, "H": 752, "I": 264, "J": 500, "K": 588, "L": 513, "M": 841, "N": 774, "O": 772, "P": 570, "Q": 776, "R": 618, "S": 617, "T": 540, "U": 709, "V": 681, "W": 950, "X": 589, "Y": 588, "Z": 644, "[": 316, "\\": 372, "]": 316, "^": 539, "_": 440, "`": 205, "a": 501, "b": 582, "c": 539, "d": 582, "e": 543, "f": 360, "g": 582, "h": 554, "i": 220, "j": 260, "k": 465, "l": 210, "m": 843, "n": 554, "o": 579, "p": 587, "q": 572, "r": 322, "s": 466, "t": 368, "u": 554, "v": 506, "w": 764, "x": 452, "y": 507, "z": 497, "{": 382, "|": 258, "}": 382, "~": 529, "–": 550, "—": 1100, "’": 166, "‘": 166, "“": 297, "”": 297, "·": 252, "…": 576, "→": 708, "←": 708, "↔": 708, "×": 620, "✓": 708, "°": 365}, "400": {" ": 247, "!": 298, "\"": 320, "#": 629, "$": 563, "%": 786, "&": 644, "'": 200, "(": 352, ")": 352, "*": 481, "+": 623, ",": 226, "-": 417, ".": 208, "/": 389, "0": 641, "1": 413, "2": 559, "3": 544, "4": 621, "5": 575, "6": 566, "7": 537, "8": 614, "9": 566, ":": 253, ";": 259, "<": 623, "=": 623, ">": 623, "?": 504, "@": 989, "A": 677, "B": 611, "C": 721, "D": 688, "E": 592, "F": 543, "G": 760, "H": 751, "I": 271, "J": 515, "K": 610, "L": 520, "M": 846, "N": 774, "O": 776, "P": 579, "Q": 780, "R": 626, "S": 614, "T": 552, "U": 707, "V": 693, "W": 960, "X": 614, "Y": 604, "Z": 641, "[": 324, "\\": 389, "]": 324, "^": 551, "_": 438, "`": 221, "a": 510, "b": 586, "c": 541, "d": 586, "e": 546, "f": 369, "g": 587, "h": 558, "i": 232, "j": 269, "k": 485, "l": 220, "m": 851, "n": 558, "o": 580, "p": 591, "q": 578, "r": 338, "s": 466, "t": 378, "u": 558, "v": 520, "w": 784, "x": 475, "y": 526, "z": 491, "{": 385, "|": 257, "}": 385, "~": 567, "–": 550, "—": 1100, "’": 181, "‘": 181, "“": 330, "”": 330, "·": 254, "…": 613, "→": 708, "←": 708, "↔": 708, "×": 623, "✓": 708, "°": 369}, "600": {" ": 241, "!": 307, "\"": 376, "#": 630, "$": 558, "%": 802, "&": 646, "'": 227, "(": 370, ")": 370, "*": 485, "+": 629, ",": 245, "-": 411, ".": 232, "/": 415, "0": 645, "1": 419, "2": 571, "3": 551, "4": 628, "5": 578, "6": 574, "7": 548, "8": 613, "9": 574, ":": 282, ";": 287, "<": 629, "=": 629, ">": 629, "?": 509, "@": 991, "A": 699, "B": 612, "C": 723, "D": 695, "E": 590, "F": 550, "G": 750, "H": 750, "I": 282, "J": 537, "K": 644, "L": 530, "M": 853, "N": 774, "O": 783, "P": 594, "Q": 785, "R": 637, "S": 610, "T": 572, "U": 705, "V": 711, "W": 975, "X": 653, "Y": 630, "Z": 635, "[": 336, "\\": 415, "]": 336, "^": 569, "_": 436, "`": 247, "a": 524, "b": 592, "c": 544, "d": 591, "e": 551, "f": 384, "g": 596, "h": 565, "i": 250, "j": 282, "k": 517, "l": 236, "m": 864, "n": 564, "o": 581, "p": 597, "q": 586, "r": 363, "s": 466, "t": 393, "u": 564, "v": 542, "w": 815, "x": 512, "y": 556, "z": 483, "{": 391, "|": 257, "}": 391, "~": 628, "–": 550, "—": 1100, "’": 204, "‘": 204, "“": 381, "”": 381, "·": 258, "…": 671, "→": 708, "←": 708, "↔": 708, "×": 629, "✓": 708, "°": 374}, "700": {" ": 238, "!": 312, "\"": 412, "#": 631, "$": 554, "%": 813, "&": 647, "'": 245, "(": 382, ")": 382, "*": 488, "+": 632, ",": 257, "-": 408, ".": 248, "/": 432, "0": 648, "1": 422, "2": 579, "3": 556, "4": 633, "5": 581, "6": 580, "7": 556, "8": 612, "9": 580, ":": 301, ";": 305, "<": 632, "=": 632, ">": 632, "?": 513, "@": 992, "A": 714, "B": 612, "C": 725, "D": 700, "E": 589, "F": 554, "G": 743, "H": 750, "I": 289, "J": 552, "K": 666, "L": 537, "M": 857, "N": 773, "O": 787, "P": 603, "Q": 789, "R": 645, "S": 607, "T": 584, "U": 704, "V": 722, "W": 985, "X": 679, "Y": 647, "Z": 632, "[": 344, "\\": 432, "]": 344, "^": 581, "_": 434, "`": 263, "a": 533, "b": 596, "c": 546, "d": 595, "e": 554, "f": 393, "g": 601, "h": 570, "i": 262, "j": 291, "k": 538, "l": 246, "m": 872, "n": 568, "o": 581, "p": 601, "q": 592, "r": 379, "s": 466, "t": 402, "u": 568, "v": 556, "w": 835, "x": 536, "y": 576, "z": 477, "{": 394, "|": 256, "}": 394, "~": 667, "–": 550, "—": 1100, "’": 219, "‘": 219, "“": 415, "”": 415, "·": 260, "…": 709, "→": 708, "←": 708, "↔": 708, "×": 632, "✓": 708, "°": 378}}""")
_WARN = []


def tw(text, size=15, weight=400):
    """Width in px of one line of Figtree text."""
    w = str(min((300, 400, 600, 700), key=lambda k: abs(k - weight)))
    table = _METRICS[w]
    return sum(table.get(c, 560) for c in text) * size / 1000


def check(lines, size, weight, maxw, where=""):
    """Record any line wider than maxw."""
    for ln in [lines] if isinstance(lines, str) else lines:
        w = tw(ln, size, weight)
        if w > maxw:
            _WARN.append(f"OVERFLOW {where}: '{ln}' is {w:.0f} px, room {maxw:.0f} px")


def report():
    for w in _WARN:
        print(w)
    if _WARN:
        sys.exit(1)


# ---------- Sunridge House Style tokens ----------
INK = "#2D2D2D"
GREY = "#6F6F6F"
OLIVE = "#61664E"
OINK = "#535349"       # olive ink: titles, arrows, step numbers
GOLD = "#D8A45F"       # accent only: the title bar, date markers, callouts
GOLD_DARK = "#B8853F"
RED = "#B5543C"        # a marker before (retyped, guessed, lost)
GREEN = "#7D8F5E"      # a marker after (kept, fixed)
SAGEL = "#DDE5DC"      # the new app
PAPER = "#F7F5F0"      # systems, label cells, panels
GLIGHT = "#CCCCCC"
GLINE = "#EEEEEE"
WHITE = "#FFFFFF"
SANS = "Figtree, 'Segoe UI', Arial, sans-serif"
SERIF = "'Libre Baskerville', Georgia, serif"
W = 1600


def esc(s):
    return escape(s, {'"': "&quot;"})


class SVG:
    def __init__(self, title, desc, h=900):
        self.h, self.title, self.desc = h, title, desc
        self.parts, self.overlay = [], []

    def add(self, s):
        self.parts.append(s)

    # ---------- primitives ----------
    def rect(self, x, y, w, h, fill=WHITE, stroke=OLIVE, sw=1.5, dash=None, opacity=None):
        a = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        self.add(a + "/>")

    def line(self, x1, y1, x2, y2, stroke=OLIVE, sw=1.5, dash=None):
        a = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"'
        self.add(a + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")

    def text(self, x, y, lines, size=14, weight=400, fill=INK, anchor="start",
             family=SANS, lh=None, italic=False, opacity=None):
        lines = [lines] if isinstance(lines, str) else lines
        lh = lh or round(size * 1.3)
        a = (f'<text x="{x}" y="{y}" font-family="{esc(family)}" font-size="{size}" '
             f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"')
        if italic:
            a += ' font-style="italic"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        a += ">" + "".join(f'<tspan x="{x}" dy="{0 if i == 0 else lh}">{esc(ln)}</tspan>'
                           for i, ln in enumerate(lines))
        self.add(a + "</text>")

    def path(self, pts, color=OINK, sw=1.6, dash=None, start=False, end=True, opacity=None):
        """An arrow through the points. color is OINK (data moves), GREY (keyed by a person, still
        open) or GLIGHT (runs alongside, fading out)."""
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        mid = {OINK: "ink", GREY: "grey", GLIGHT: "light"}[color]
        a = f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if end:
            a += f' marker-end="url(#ah-{mid})"'
        if start:
            a += f' marker-start="url(#ah-{mid})"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        self.add(a + "/>")

    def badge(self, cx, cy, label, color, r=15):
        """A marker circle (R1, D2...). Drawn last, so arrows never run over it."""
        keep, self.parts = self.parts, self.overlay
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>')
        self.text(cx, cy + 5, label, size=14, weight=700, fill=WHITE, anchor="middle")
        self.parts = keep

    def stepnum(self, x, y, n, fill=OINK):
        """Square step number on a box's top-left corner."""
        self.rect(x - 11, y - 11, 22, 22, fill=fill, stroke=None)
        self.text(x, y + 5, str(n), size=14, weight=700, fill=WHITE, anchor="middle")

    def diamond(self, cx, cy, w, h, lines, size=14):
        pts = f"{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}"
        self.add(f'<polygon points="{pts}" fill="{WHITE}" stroke="{OLIVE}" stroke-width="1.5"/>')
        check(lines, size, 600, w * 0.62, f"diamond {lines[0]}")
        self.text(cx, cy - (len(lines) - 1) * 8.5 + 5, lines, size=size, weight=600, anchor="middle", lh=17)

    # ---------- page furniture ----------
    def header(self, section, topic, takeaway):
        """'Section | Topic' in Baskerville with the gold bar, a one-line takeaway, the Draft tag."""
        self.add(f'<text x="40" y="58" font-family="{esc(SERIF)}" font-size="28" fill="{OINK}">'
                 f'{esc(section)} <tspan fill="{GOLD}">|</tspan> '
                 f'<tspan font-style="italic">{esc(topic)}</tspan></text>')
        check(takeaway, 18, 300, 1520, "takeaway")
        self.text(40, 92, takeaway, size=18, weight=300)
        self.rect(1490, 34, 70, 28, fill=WHITE, stroke=GREY, sw=1)
        self.text(1525, 53, "Draft", size=14, weight=600, fill=GREY, anchor="middle")

    def footer(self, source):
        y = self.h - 48
        self.line(40, y, 1560, y, stroke=GLINE, sw=1)
        check(source, 14, 400, 1280, "source line")
        self.text(40, y + 26, source, size=14, fill=GREY)
        self.text(1560, y + 26, "2026 / Strictly confidential", size=14, fill=GREY, anchor="end")

    def render(self):
        defs = "".join(f'<marker id="ah-{m}" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" '
                       f'markerWidth="11" markerHeight="11" orient="auto-start-reverse">'
                       f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
                       for m, c in (("ink", OINK), ("grey", GREY), ("light", GLIGHT)))
        body = "\n".join(self.parts + self.overlay)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {self.h}" width="{W}" height="{self.h}" '
                f'role="img" aria-labelledby="t d">\n<title id="t">{esc(self.title)}</title>\n'
                f'<desc id="d">{esc(self.desc)}</desc>\n<defs>{defs}</defs>\n'
                f'<rect x="0" y="0" width="{W}" height="{self.h}" fill="{WHITE}"/>\n{body}\n</svg>\n')

    def save(self, path):
        with open(path, "w") as f:
            f.write(self.render())


# ---------- layout helpers ----------
def box(s, b, title, sub=None, fill=WHITE, opacity=None, dash=None):
    """A party (WHITE), a system (PAPER) or the app (SAGEL): bold title, grey sub-lines. b = (x, y, w, h)."""
    x, y, w, h = b
    s.rect(x, y, w, h, fill=fill, opacity=opacity, dash=dash)
    check(title, 18, 600, w - 28, f"box {title}")
    s.text(x + 16, y + 30, title, size=18, weight=600, opacity=opacity)
    if sub:
        sub = [sub] if isinstance(sub, str) else sub
        check(sub, 15, 400, w - 28, f"box {title} sub")
        s.text(x + 16, y + 54, sub, size=15, fill=GREY, lh=19, opacity=opacity)
        if 54 + 19 * (len(sub) - 1) + 10 > h:
            _WARN.append(f"OVERFLOW box {title}: sub-lines run below the box")


def label(s, x, y, lines, anchor="middle", maxw=260, **kw):
    """An arrow label, measured."""
    check(lines, kw.get("size", 14), kw.get("weight", 400), maxw, f"label {lines}")
    s.text(x, y, lines, anchor=anchor, size=kw.pop("size", 14), lh=kw.pop("lh", 17), **kw)


def panel(s, b, title, rows, title2=None, rows2=None):
    """The side panel: 'Where it breaks' before, 'What changed' after (and optionally 'Still open')."""
    x, y, w, h = b
    s.rect(x, y, w, h, fill=PAPER, stroke=None)
    s.line(x, y, x + w, y, stroke=OLIVE, sw=2)
    yy = y + 32
    for t, rs in ((title, rows), (title2, rows2)):
        if not t:
            continue
        s.text(x + 16, yy, t, size=19, family=SERIF, fill=OINK, italic=True)
        yy += 28
        for r in rs:
            r = [r] if isinstance(r, str) else r
            check(r, 15, 400, w - 56, f"panel {t}")
            s.rect(x + 22, yy - 9, 8, 8, fill=OLIVE, stroke=None)
            s.text(x + 40, yy, r, size=15, lh=19)
            yy += 19 * len(r) + 14
        yy += 16
    if yy - 16 > y + h:
        _WARN.append(f"OVERFLOW panel {title}: rows run below the panel")


LX, LW, RIGHT, TOP = 40, 130, 1575, 108


def lanes(s, spec, app_key="app", app_active=True):
    """Swimlanes. spec: [(key, [name lines], height)]. Returns {key: centre y}.
    The app lane is sage when the app exists, greyed when drawing the before."""
    y, out = TOP, {}
    for key, name, h in spec:
        band, cell, txt = WHITE, PAPER, INK
        if key == app_key:
            band, cell, txt = (WHITE, SAGEL, OINK) if app_active else ("#F4F4F4", GLINE, GREY)
        s.rect(LX, y, RIGHT - LX, h, fill=band, stroke=None)
        s.rect(LX, y, LW, h, fill=cell, stroke=None)
        s.text(LX + 12, y + h / 2 - (len(name) - 1) * 9 + 5, name, size=15, weight=600, fill=txt, lh=18)
        s.line(LX, y + h, RIGHT, y + h, stroke=GLIGHT, sw=1)
        out[key] = y + h / 2
        y += h
    s.line(LX, TOP, RIGHT, TOP, stroke=OLIVE, sw=2)
    s.line(LX, y, RIGHT, y, stroke=OLIVE, sw=2)
    return out


def step(s, n, cx, cy, w, h, lines, fill=WHITE):
    """A process step centred on (cx, cy); n is its number from the brief, or None.
    fill=SAGEL for a step the app does."""
    s.rect(cx - w / 2, cy - h / 2, w, h, fill=fill)
    check(lines, 14, 500 if fill == SAGEL else 400, w - 16, f"step {n}")
    s.text(cx + (3 if n is not None else 0), cy - (len(lines) - 1) * 8.5 + 5, lines, size=14,
           anchor="middle", lh=17, weight=500 if fill == SAGEL else 400)
    if n is not None:
        s.stepnum(cx - w / 2, cy - h / 2, n)


def chip(s, cx, cy, w, h, lines, faded=False):
    """What lands in a system (PAPER); faded=True for one that runs alongside until a switch."""
    if faded:
        s.rect(cx - w / 2, cy - h / 2, w, h, fill=PAPER, stroke=GREY, dash="4 3", opacity=0.75)
    else:
        s.rect(cx - w / 2, cy - h / 2, w, h, fill=PAPER)
    check(lines, 14, 400, w - 12, f"chip {lines[0]}")
    s.text(cx, cy - (len(lines) - 1) * 8.5 + 5, lines, size=14, fill=GREY if faded else INK, anchor="middle", lh=17)


def legend(s, items, y, x=40):
    """items: (kind, label). Kinds: party, system, app, faded, arrow, keyed, loop, step, decision,
    chip, callout, or ('badge', letter, colour)."""
    for kind, text in items:
        if isinstance(kind, tuple):
            s.badge(x + 13, y - 4, kind[1], kind[2], r=13); x += 32
        elif kind == "party":
            s.rect(x, y - 13, 28, 18); x += 36
        elif kind == "system":
            s.rect(x, y - 13, 28, 18, fill=PAPER); x += 36
        elif kind == "app":
            s.rect(x, y - 13, 28, 18, fill=SAGEL); x += 36
        elif kind == "faded":
            s.rect(x, y - 13, 28, 18, fill=PAPER, stroke=GREY, dash="4 3", opacity=0.6); x += 36
        elif kind == "arrow":
            s.path([(x, y - 4), (x + 36, y - 4)]); x += 46
        elif kind == "keyed":
            s.path([(x, y - 4), (x + 36, y - 4)], color=GREY, dash="6 4"); x += 46
        elif kind == "loop":
            s.path([(x, y - 4), (x + 36, y - 4)], dash="5 4"); x += 46
        elif kind == "step":
            s.rect(x, y - 13, 30, 18); s.rect(x - 5, y - 18, 12, 12, fill=OINK, stroke=None); x += 40
        elif kind == "decision":
            s.add(f'<polygon points="{x + 15},{y - 16} {x + 30},{y - 4} {x + 15},{y + 8} {x},{y - 4}" '
                  f'fill="{WHITE}" stroke="{OLIVE}" stroke-width="1.5"/>'); x += 40
        elif kind == "chip":
            s.rect(x, y - 13, 30, 18, fill=PAPER); x += 40
        elif kind == "callout":
            s.rect(x, y - 13, 28, 18, fill=WHITE, stroke=GOLD); s.rect(x, y - 13, 5, 18, fill=GOLD, stroke=None); x += 36
        s.text(x, y + 1, text, size=14)
        x += tw(text, 14) + 28
