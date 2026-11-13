"""Worked example: a data flow, before and after, for an invented company (Acme, order intake).

Copy this file, keep the shape, replace the boxes, arrows and markers with the real case:
  python3 example_dataflow.py out/   ->  out/data-flow-before.svg, out/data-flow-after.svg
Both diagrams share one geometry, so a reader flipping Before/After sees what moved, not a new layout.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import *  # noqa: E402,F403

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
SOURCE = "Source: Acme ordering brief, Sep 2026 (invented example)"

# One geometry for both diagrams: (x, y, w, h)
CUST = (40, 170, 210, 200)
CLERK = (420, 170, 230, 100)
LEAD = (420, 590, 230, 90)
ERP = (1060, 170, 240, 140)
REPORT = (1060, 370, 240, 110)
SHEET = (1060, 590, 240, 90)
SUPP = (1400, 170, 170, 90)
APP = (700, 340, 240, 150)
PANEL = (40, 480, 330, 260)


def common(s, after):
    box(s, CUST, "Customer", ["sends orders by", "email, PDF or phone"])
    box(s, CLERK, "Order clerk", "keys orders and dates" if not after else ["confirms, keys the ERP", "once"])
    box(s, LEAD, "Planning lead", "checks the plan")
    box(s, ERP, "ERP", ["orders, POs;", "never written by the app"] if after else ["orders, POs;", "dates often blank"], fill=PAPER)
    box(s, REPORT, "Stock report", ["refreshed overnight"], fill=PAPER)
    if after:
        box(s, SHEET, "Plan spreadsheet", ["runs alongside until", "the switch"], fill=PAPER, opacity=0.5, dash="5 4")
    else:
        box(s, SHEET, "Plan spreadsheet", ["retyped; drifts from", "the ERP"], fill=PAPER)
    box(s, SUPP, "Supplier", ["gets POs, sends", "date changes"])
    s.path([(250, 200), (420, 200)])
    s.path([(1300, 215), (1400, 215)])
    label(s, 1350, 205, "PO", maxw=90)
    s.path([(1180, 310), (1180, 370)])
    label(s, 1170, 334, ["overnight extract"], anchor="end", maxw=200)


def before():
    s = SVG("Acme data flow before the ordering app",
            "How orders, stock and dates moved before the app: three manual re-keys (R1-R3) and two places a date got lost (D1-D2).")
    s.header("Acme ordering", "Data flow before (Sep 2026)",
             "Each order is typed by hand up to three times, and two dates live only in inboxes.")
    common(s, after=False)
    label(s, 335, 174, ["orders in any shape"], maxw=170)
    s.path([(650, 205), (1060, 205)])
    label(s, 855, 195, "typed by hand", maxw=300)
    s.path([(1060, 430), (560, 430), (560, 270)])
    label(s, 810, 420, "read order by order, up to a day old", maxw=420)
    s.path([(650, 640), (1060, 640)])
    label(s, 855, 628, "order, line, shift retyped", maxw=380)
    s.path([(1570, 240), (1588, 240), (1588, 728), (535, 728), (535, 680)])
    label(s, 1000, 718, "new dates by email, often not keyed", anchor="start", maxw=520)
    s.badge(690, 236, "R1", RED)
    s.badge(700, 640, "R2", RED)
    s.badge(335, 248, "D1", GOLD)
    s.badge(980, 728, "D2", GOLD)
    panel(s, PANEL, "Where it breaks", [["Data up to a day old"], ["2 re-keys per order (R1-R2)"],
                                         ["2 places dates get lost (D1-D2)"], ["No record of why a date moved"]])
    legend(s, [("party", "Person or party"), ("system", "System"), ("arrow", "Data moves"),
               (("badge", "R", RED), "Manual re-key"), (("badge", "D", GOLD), "Date lost")], 807)
    s.footer(SOURCE)
    return s


def after():
    s = SVG("Acme data flow after the ordering app",
            "How data moves since the app went live: the app reads the ERP every 15 minutes, read-only; a person still keys the ERP once by design.")
    s.header("Acme ordering", "Data flow after (live since Oct 2026)",
             "The app re-reads the ERP every 15 minutes and keeps one short list; keying stays with a person.")
    common(s, after=True)
    box(s, APP, "Ordering app", ["stock check every 15 min;", "one list: what, by when,", "who acts"], fill=SAGEL)
    label(s, 335, 174, ["orders in any shape"], maxw=170)
    s.path([(650, 205), (1060, 205)], color=GREY, dash="7 5")
    label(s, 855, 195, "keyed by a person (by design)", weight=600, maxw=300)
    s.path([(1060, 430), (940, 430)])
    label(s, 1000, 418, "every 15 min", maxw=110)
    s.path([(560, 270), (560, 390), (700, 390)], start=True)
    s.path([(650, 640), (1060, 640)], color=GLIGHT, dash="6 4")
    label(s, 855, 628, "still updated by hand until the switch", fill=GREY, maxw=380)
    s.path([(1570, 240), (1588, 240), (1588, 728), (535, 728), (535, 680)])
    label(s, 900, 718, "new dates kept as date events with a reason", anchor="start", maxw=620)
    s.badge(690, 236, "R1", GREY)
    s.badge(700, 640, "R2", GREY)
    s.badge(335, 248, "D1", GREEN)
    s.badge(880, 728, "D2", GREEN)
    panel(s, PANEL, "What changed", [["Stock re-checked every 15 min"], ["One list: what, by when, who acts"],
                                      ["Dates kept with a reason"], ["Still by hand: keying the ERP"]])
    legend(s, [("party", "Person or party"), ("system", "System"), ("app", "Ordering app"),
               ("keyed", "Keyed by a person"), ("faded", "Runs alongside"),
               (("badge", "D", GREEN), "Date now kept"), (("badge", "R", GREY), "Re-key left by hand")], 807)
    s.footer(SOURCE)
    return s


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    before().save(os.path.join(OUT, "data-flow-before.svg"))
    after().save(os.path.join(OUT, "data-flow-after.svg"))
    report()
    print("wrote", OUT)
