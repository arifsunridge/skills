"""Worked example: a swimlane process, before and after, for an invented company (Acme, order intake).

Copy this file, keep the shape, replace lanes and steps with the real case:
  python3 example_process.py out/   ->  out/process-before.svg, out/process-after.svg
Steps carry the numbers from the brief; the same lanes appear on both, the app lane greyed before.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import *  # noqa: E402,F403

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
SOURCE = "Source: Acme ordering brief, Sep 2026 (invented example). Box = step in the lane of who does it."
LANES = [("cust", ["Customer"], 80), ("clerk", ["Order clerk"], 120), ("lead", ["Planning lead"], 100),
         ("app", ["Ordering app"], 110), ("erp", ["ERP"], 90), ("sheet", ["Plan", "spreadsheet"], 80),
         ("supp", ["Supplier"], 80)]
BW, BH = 170, 54


def before():
    s = SVG("Acme process before the ordering app",
            "Swimlane of how an order was handled before the app, steps 1-7: retyped into the ERP, stock read "
            "from an overnight report, shortages chased by email, the plan retyped; any change restarts steps 2-6.")
    s.header("Acme ordering", "Process before (Sep 2026)",
             "Every order passes seven hand steps; any date change restarts steps 2-6 with no record of why.")
    L = lanes(s, LANES, app_active=False)
    s.text(960, L["app"] + 5, "No app: no single list of what is short",
           size=14, fill=GREY, anchor="middle", italic=True)
    chip(s, 290, L["cust"], 190, 44, ["Order: PDF, email, phone"])
    step(s, 1, 290, L["clerk"], BW, BH, ["Retype the order", "into the ERP"])
    s.path([(290, L["cust"] + 22), (290, L["clerk"] - BH / 2)])
    chip(s, 290, L["erp"], 150, 40, ["Order"])
    s.path([(290, L["clerk"] + BH / 2), (290, L["erp"] - 20)])
    s.badge(320, L["clerk"] + 50, "R1", RED)
    step(s, 2, 520, L["clerk"], BW, BH, ["Read stock report,", "order by order"])
    s.path([(375, L["clerk"]), (435, L["clerk"])])
    s.diamond(730, L["clerk"], 160, 84, ["Enough", "stock?"])
    s.path([(605, L["clerk"]), (650, L["clerk"])])
    step(s, 3, 730, L["supp"], BW, BH, ["Email the supplier", "for a date"])
    s.path([(730, L["clerk"] + 42), (730, L["supp"] - BH / 2)])
    label(s, 742, L["lead"] + 5, "no", anchor="start", fill=GREY, maxw=40)
    step(s, 4, 960, L["clerk"], BW, BH, ["Key the date,", "when remembered"])
    s.path([(810, L["clerk"]), (875, L["clerk"])])
    label(s, 842, L["clerk"] - 10, "yes", fill=GREY, maxw=40)
    s.badge(960, L["clerk"] + 50, "D1", GOLD)
    step(s, 5, 1190, L["lead"], BW, BH, ["Retype order, line,", "shift into the plan"])
    s.path([(1045, L["clerk"]), (1190, L["clerk"]), (1190, L["lead"] - BH / 2)])
    chip(s, 1190, L["sheet"], 170, 44, ["Shift plan; drifts"])
    s.path([(1190, L["lead"] + BH / 2), (1190, L["sheet"] - 22)])
    s.badge(1220, L["lead"] + 50, "R2", RED)
    step(s, 6, 1420, L["cust"], BW, BH, ["Tell the customer", "the date"])
    s.path([(1275, L["lead"]), (1420, L["lead"]), (1420, L["cust"] + BH / 2)])
    # The redo loop: any change from the customer sends the order back to step 2.
    s.path([(1505, L["cust"]), (1550, L["cust"]), (1550, L["clerk"] - 54), (520, L["clerk"] - 54),
            (520, L["clerk"] - BH / 2)], dash="5 4")
    label(s, 1000, L["clerk"] - 62, "date or qty changes: steps 2-6 redone by hand, no record of why", maxw=560)
    legend(s, [("step", "Step (number as in the brief)"), ("decision", "Decision"), ("chip", "What lands in a system"),
               (("badge", "R", RED), "Manual re-key"), (("badge", "D", GOLD), "Date lost"), ("loop", "Redo loop")], 822)
    s.footer(SOURCE)
    return s


def after():
    s = SVG("Acme process after the ordering app",
            "Swimlane of how an order is handled since the app went live, steps 1-6: the app checks stock every 15 "
            "minutes and drafts each route, the clerk confirms and keys the ERP once, every date move is kept.")
    s.header("Acme ordering", "Process after (live since Oct 2026)",
             "The app checks stock and drafts each route; people confirm, key the ERP and send.")
    L = lanes(s, LANES, app_active=True)
    chip(s, 290, L["cust"], 190, 44, ["Order: PDF, email, phone"])
    step(s, 1, 290, L["app"], BW, BH, ["Order dropped in,", "read by rules"], fill=SAGEL)
    s.path([(290, L["cust"] + 22), (290, L["app"] - BH / 2)])
    step(s, 2, 520, L["app"], BW, BH, ["Check stock", "every 15 min"], fill=SAGEL)
    s.path([(375, L["app"]), (435, L["app"])])
    s.diamond(730, L["app"], 160, 84, ["Enough", "stock?"])
    s.path([(605, L["app"]), (650, L["app"])])
    step(s, 3, 730, L["supp"], BW, BH, ["Supplier ask", "drafted by the app"])
    s.path([(730, L["app"] + 42), (730, L["supp"] - BH / 2)])
    label(s, 742, L["erp"] + 5, "no", anchor="start", fill=GREY, maxw=40)
    label(s, 842, L["app"] - 10, "yes", fill=GREY, maxw=40)
    step(s, 4, 960, L["clerk"], BW, BH, ["Confirm; key the", "ERP once"])
    s.path([(810, L["app"]), (915, L["app"]), (915, L["clerk"] + BH / 2)])
    chip(s, 1010, L["erp"], 150, 40, ["Order, date"])
    s.path([(1010, L["clerk"] + BH / 2), (1010, L["erp"] - 20)], color=GREY, dash="6 4")
    s.badge(1040, L["app"], "R1", GREY)
    step(s, 5, 1190, L["lead"], BW, BH, ["Place on the plan", "in the app"])
    s.path([(1045, L["clerk"]), (1190, L["clerk"]), (1190, L["lead"] - BH / 2)])
    chip(s, 1190, L["sheet"], 170, 44, ["Until the switch"], faded=True)
    s.path([(1190, L["lead"] + BH / 2), (1190, L["sheet"] - 22)], color=GLIGHT, dash="6 4")
    step(s, 6, 1420, L["cust"], BW, BH, ["Send the drafted", "date message"])
    s.path([(1275, L["lead"]), (1420, L["lead"]), (1420, L["cust"] + BH / 2)])
    s.text(1420, L["app"] + 5, "Every date move: event + reason", size=14, anchor="middle", fill=OINK)
    s.badge(1265, L["app"], "D1", GREEN)
    legend(s, [("step", "Step"), ("app", "Done by the app"), ("decision", "Decision"), ("chip", "In a system"),
               ("keyed", "Keyed by a person"), ("faded", "Runs alongside"), (("badge", "D", GREEN), "Date now kept")], 822)
    s.footer(SOURCE)
    return s


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    before().save(os.path.join(OUT, "process-before.svg"))
    after().save(os.path.join(OUT, "process-after.svg"))
    report()
    print("wrote", OUT)
