from __future__ import annotations

import os
import sys
from datetime import date, datetime, timedelta
from typing import List, Tuple

from flask import Flask, render_template, request, redirect, url_for, Response, session


# Ensure parent directory (Study) is importable to reuse smoke_counter.py
THIS_DIR = os.path.dirname(__file__)
STUDY_DIR = os.path.dirname(THIS_DIR)
if STUDY_DIR not in sys.path:
    sys.path.insert(0, STUDY_DIR)

import smoke_counter as sc  # type: ignore


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SMOKE_COUNTER_SECRET", "dev-secret-change-me")


def _pin_required() -> bool:
    return bool(os.environ.get("SMOKE_COUNTER_PIN"))


@app.before_request
def _require_login():
    # If a PIN is configured, require auth for all routes except login and static
    if not _pin_required():
        return None
    endpoint = request.endpoint or ""
    if endpoint in ("login", "static"):
        return None
    if session.get("authed"):
        return None
    # preserve next URL
    return redirect(url_for("login", next=request.path))


def _recent_events(store: sc.Store, limit: int = 10) -> List[Tuple[str, str, bool]]:
    rows: List[Tuple[str, str, bool]] = []
    for d, events in store.events.items():
        for e in events:
            rows.append((d, e.get("time", "00:00"), bool(e.get("relapse", False))))
    rows.sort(key=lambda r: (r[0], r[1]))
    if limit and limit > 0:
        rows = rows[-limit:]
    return rows


@app.route("/")
def index():
    store = sc.load_store()
    stats = sc.compute_stats(store)
    weekly_best = sc.compute_weekly_best_success_streak(store)
    recent = _recent_events(store, 10)
    # Last 30 days timeline
    today = date.today()
    last30_labels: List[str] = []
    last30_counts: List[int] = []
    last30_relapses: List[int] = []
    for i in range(29, -1, -1):
        d = today - timedelta(days=i)
        key = d.isoformat()
        events = store.events.get(key, [])
        last30_labels.append(key)
        last30_counts.append(len(events))
        last30_relapses.append(sum(1 for e in events if e.get("relapse")))

    # Current month heatmap data
    ym = today.strftime("%Y-%m")
    m_start, m_end = sc.month_range(ym)
    month_days = []
    dcur = m_start
    while dcur <= m_end:
        key = dcur.isoformat()
        events = store.events.get(key, [])
        month_days.append({
            "iso": key,
            "day": dcur.day,
            "weekday": dcur.weekday(),  # 0=Mon
            "count": len(events),
            "relapses": sum(1 for e in events if e.get("relapse")),
        })
        dcur += timedelta(days=1)
    month_max = max((day["count"] for day in month_days), default=0)
    return render_template(
        "index.html",
        stats=stats,
        weekly_best=weekly_best,
        recent=recent,
        last30_labels=last30_labels,
        last30_counts=last30_counts,
        last30_relapses=last30_relapses,
        month_days=month_days,
        month_max=month_max,
        pin_required=_pin_required(),
        authed=session.get("authed", False),
    )


@app.route("/log", methods=["POST"])
def log_event():
    store = sc.load_store()
    d = request.form.get("date") or None
    t = request.form.get("time") or None
    relapse = request.form.get("relapse") == "on"
    d, t = sc.add_event(store, d, t, relapse=relapse)
    if not store.start_date:
        store.start_date = d
    sc.save_store(store)
    return redirect(url_for("index"))


@app.route("/weekly")
def weekly():
    store = sc.load_store()
    dparam = request.args.get("date")
    try:
        day = datetime.strptime(dparam, "%Y-%m-%d").date() if dparam else date.today()
    except ValueError:
        day = date.today()
    summary = sc.summarize_week(store, day)
    return render_template("weekly.html", summary=summary)


@app.route("/weekly.csv")
def weekly_csv():
    store = sc.load_store()
    dparam = request.args.get("date")
    try:
        day = datetime.strptime(dparam, "%Y-%m-%d").date() if dparam else date.today()
    except ValueError:
        day = date.today()
    summary = sc.summarize_week(store, day)
    # Build CSV text
    lines = ["date,count,relapse_count"]
    for d, c in summary["day_counts"]:
        relapses = sum(1 for e in store.events.get(d, []) if e.get("relapse"))
        lines.append(f"{d},{c},{relapses}")
    csv_text = "\n".join(lines) + "\n"
    return Response(csv_text, mimetype="text/csv")


@app.route("/monthly")
def monthly():
    store = sc.load_store()
    ym = request.args.get("month") or date.today().strftime("%Y-%m")
    try:
        summary = sc.summarize_month(store, ym)
    except ValueError:
        summary = sc.summarize_month(store, date.today().strftime("%Y-%m"))
    weekly_best = sc.compute_weekly_best_success_streak(store)
    return render_template("monthly.html", summary=summary, weekly_best=weekly_best)


@app.route("/monthly.csv")
def monthly_csv():
    store = sc.load_store()
    ym = request.args.get("month") or date.today().strftime("%Y-%m")
    summary = sc.summarize_month(store, ym)
    lines = ["date,count,relapse_count"]
    for d, c in summary["day_counts"]:
        relapses = sum(1 for e in store.events.get(d, []) if e.get("relapse"))
        lines.append(f"{d},{c},{relapses}")
    csv_text = "\n".join(lines) + "\n"
    return Response(csv_text, mimetype="text/csv")


@app.route("/login", methods=["GET", "POST"])
def login():
    # If no PIN configured, bypass login
    if not _pin_required():
        session["authed"] = True
        return redirect(url_for("index"))
    error = None
    next_url = request.args.get("next") or url_for("index")
    if request.method == "POST":
        pin = request.form.get("pin", "")
        if pin == os.environ.get("SMOKE_COUNTER_PIN"):
            session["authed"] = True
            return redirect(next_url)
        else:
            error = "Invalid PIN"
    return render_template("login.html", error=error, next_url=next_url)


@app.route("/logout")
def logout():
    session.clear()
    if _pin_required():
        return redirect(url_for("login"))
    return redirect(url_for("index"))


@app.route("/delete", methods=["POST"])
def delete_event():
    store = sc.load_store()
    d = request.form.get("date")
    t = request.form.get("time")
    if d and t:
        sc.remove_event(store, d, t)
        sc.save_store(store)
    return redirect(url_for("index"))


@app.route("/edit", methods=["POST"])
def edit_event():
    store = sc.load_store()
    old_date = request.form.get("old_date")
    old_time = request.form.get("old_time")
    new_date = request.form.get("date") or None
    new_time = request.form.get("time") or None
    relapse_str = request.form.get("relapse")
    relapse = None
    if relapse_str is not None:
        # Checkbox: 'on' when checked; we also support explicit 'true'/'false'
        relapse = True if relapse_str in ("on", "true", "1") else False
    if old_date and old_time:
        sc.edit_event(store, old_date, old_time, new_date, new_time, relapse)
        sc.save_store(store)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Run: python Study/smoke_counter_web/app.py
    app.run(host="127.0.0.1", port=5000, debug=True)
