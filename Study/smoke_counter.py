"""
Smoke counter CLI

Track smoke events and see your smoke-free streak and stats.

Data model (JSON at Study/smoke_counter_data.json):
{
  "start_date": "YYYY-MM-DD" | null,
	"events": { "YYYY-MM-DD": [{"time": "HH:MM", "relapse": bool}, ...], ... },
	"daily_goal": 0  # max allowed events per day to count as a "success" day
}

Commands:
  - init [--start YYYY-MM-DD]        Initialize tracking start date
  - log [--date YYYY-MM-DD] [--time HH:MM]   Record a smoke event (default: now)
							[--relapse]                    Mark this event as a relapse
  - status                           Show streak and totals
  - list [--limit N]                 Show recent events
  - undo                             Remove the most recent event
	- goal [--set N]                   View or set daily goal
	- summary [--month YYYY-MM]        Monthly summary and weekly best streak
  - weekly [--date YYYY-MM-DD]       Weekly summary for the week containing date
	- tui                               Simple interactive text UI
to activate the virtual environment and run the app:
source Study/smoke_counter_web/.venv/bin/activate                                                12:10 
python Study/smoke_counter_web/app.py
"""

from __future__ import annotations

import argparse
import json
import os
import csv
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple


# Store data alongside this script
DATA_FILE = os.path.join(os.path.dirname(__file__), "smoke_counter_data.json")


@dataclass
class Store:
	start_date: Optional[str]
	# events: date -> list of event dicts: {"time": "HH:MM", "relapse": bool}
	events: Dict[str, List[dict]]
	daily_goal: int = 0

	@staticmethod
	def empty() -> "Store":
		return Store(start_date=None, events={})


def load_store() -> Store:
	if not os.path.exists(DATA_FILE):
		return Store.empty()
	try:
		with open(DATA_FILE, "r", encoding="utf-8") as f:
			data = json.load(f)
		# Basic validation
		start_date = data.get("start_date")
		events = data.get("events", {})
		daily_goal = int(data.get("daily_goal", 0) or 0)
		if not isinstance(events, dict):
			events = {}
		# Normalize events to list of dicts with keys: time, relapse
		norm_events: Dict[str, List[dict]] = {}
		for d, times in events.items():
			if not isinstance(times, list):
				continue
			day_list: List[dict] = []
			for t in times:
				if isinstance(t, dict):
					time_str = _normalize_time_str(t.get("time", "00:00"))
					relapse = bool(t.get("relapse", False))
				else:
					# legacy: just a time string
					time_str = _normalize_time_str(str(t))
					relapse = False
				day_list.append({"time": time_str, "relapse": relapse})
			# sort by time
			day_list.sort(key=lambda r: r.get("time", "00:00"))
			norm_events[d] = day_list
		return Store(start_date=start_date, events=norm_events, daily_goal=daily_goal)
	except Exception:
		# On any error, start fresh rather than crashing
		return Store.empty()


def save_store(store: Store) -> None:
	# Ensure events are normalized to list of dicts
	normalized_events: Dict[str, List[dict]] = {}
	for d, times in store.events.items():
		day_list: List[dict] = []
		for t in times or []:
			if isinstance(t, dict):
				time_str = _normalize_time_str(t.get("time", "00:00"))
				relapse = bool(t.get("relapse", False))
			else:
				time_str = _normalize_time_str(str(t))
				relapse = False
			day_list.append({"time": time_str, "relapse": relapse})
		day_list.sort(key=lambda r: r.get("time", "00:00"))
		normalized_events[d] = day_list
	tmp = {
		"start_date": store.start_date,
		"events": normalized_events,
		"daily_goal": int(getattr(store, "daily_goal", 0) or 0),
	}
	with open(DATA_FILE, "w", encoding="utf-8") as f:
		json.dump(tmp, f, indent=2, ensure_ascii=False)


# ---------- Helpers ----------


def today_str() -> str:
	return date.today().isoformat()


def now_time_str() -> str:
	return datetime.now().strftime("%H:%M")


def _normalize_date_str(s: str) -> str:
	# Accept YYYY-MM-DD; raise if invalid
	return datetime.strptime(s, "%Y-%m-%d").date().isoformat()


def _normalize_time_str(s: str) -> str:
	# Accept HH:MM (24h)
	return datetime.strptime(s.strip(), "%H:%M").strftime("%H:%M")


def month_range(ym: str) -> Tuple[date, date]:
	"""Return the first and last date of a given YYYY-MM month."""
	start = datetime.strptime(ym + "-01", "%Y-%m-%d").date()
	# next month trick: add 32 days then go to 1st and step back
	next_month_first = (start.replace(day=1) + timedelta(days=32)).replace(day=1)
	last = next_month_first - timedelta(days=1)
	return start, last


def week_start(d: date) -> date:
	"""Return Monday of the week containing d."""
	return d - timedelta(days=d.weekday())


def summarize_week(store: Store, some_day: date) -> Dict[str, object]:
	"""Summarize the Monday..Sunday week containing some_day."""
	start = week_start(some_day)
	end = start + timedelta(days=6)
	goal = int(getattr(store, "daily_goal", 0) or 0)

	events_total = 0
	success_days = 0
	smoke_free_days = 0
	day_counts: List[Tuple[str, int]] = []
	best_streak = 0
	cur_streak = 0

	dcur = start
	while dcur <= end:
		key = dcur.isoformat()
		cnt = len(store.events.get(key, []))
		events_total += cnt
		if cnt == 0:
			smoke_free_days += 1
		is_success = cnt <= goal
		if is_success:
			success_days += 1
			cur_streak += 1
			best_streak = max(best_streak, cur_streak)
		else:
			cur_streak = 0
		day_counts.append((key, cnt))
		dcur += timedelta(days=1)

	avg_per_day = round(events_total / 7, 2)
	success_rate = round((success_days / 7) * 100, 1)
	return {
		"week_start": start.isoformat(),
		"week_end": end.isoformat(),
		"events_total": events_total,
		"avg_per_day": avg_per_day,
		"smoke_free_days": smoke_free_days,
		"success_days": success_days,
		"success_rate": success_rate,
		"daily_goal": goal,
		"best_streak": best_streak,
		"day_counts": day_counts,
	}


def compute_weekly_best_success_streak(store: Store) -> int:
	"""Compute the best weekly (Mon-Sun) streak where each day is a 'success' day under daily_goal.

	A streak is consecutive success days; we report the maximum length found within any Monday..Sunday window.
	"""
	if not store.start_date:
		return 0
	try:
		start = datetime.strptime(store.start_date, "%Y-%m-%d").date()
	except ValueError:
		return 0
	today = date.today()
	goal = int(getattr(store, "daily_goal", 0) or 0)

	# Build a map of day->success flag
	success: Dict[date, bool] = {}
	dcur = start
	while dcur <= today:
		cnt = len(store.events.get(dcur.isoformat(), []))
		success[dcur] = (cnt <= goal)
		dcur += timedelta(days=1)

	# Iterate weeks from first Monday up to the current week
	first_monday = week_start(start)
	cur = first_monday
	best = 0
	while cur <= today:
		# Window Monday..Sunday
		streak = 0
		for i in range(7):
			day = cur + timedelta(days=i)
			ok = success.get(day, False)
			if ok:
				streak += 1
				if streak > best:
					best = streak
			else:
				streak = 0
		cur += timedelta(days=7)
	return best


def summarize_month(store: Store, ym: str) -> Dict[str, object]:
	"""Monthly summary keyed by YYYY-MM."""
	start, end = month_range(ym)
	goal = int(getattr(store, "daily_goal", 0) or 0)

	days = (end - start).days + 1
	events_total = 0
	success_days = 0
	smoke_free_days = 0
	day_counts: List[Tuple[str, int]] = []

	dcur = start
	while dcur <= end:
		key = dcur.isoformat()
		cnt = len(store.events.get(key, []))
		events_total += cnt
		if cnt == 0:
			smoke_free_days += 1
		if cnt <= goal:
			success_days += 1
		day_counts.append((key, cnt))
		dcur += timedelta(days=1)

	avg_per_day = round(events_total / days, 2) if days else 0.0
	success_rate = round((success_days / days) * 100, 1) if days else 0.0
	return {
		"month": ym,
		"days_in_month": days,
		"events_total": events_total,
		"avg_per_day": avg_per_day,
		"smoke_free_days": smoke_free_days,
		"success_days": success_days,
		"success_rate": success_rate,
		"daily_goal": goal,
		"day_counts": day_counts,  # list of (YYYY-MM-DD, count)
	}


def add_event(store: Store, d: Optional[str] = None, t: Optional[str] = None, relapse: bool = False) -> Tuple[str, str]:
	d = _normalize_date_str(d) if d else today_str()
	t = _normalize_time_str(t) if t else now_time_str()
	day_list = store.events.setdefault(d, [])
	# dedupe by time; if exists, update relapse to True if either marked
	existing = next((e for e in day_list if e.get("time") == t), None)
	if existing:
		existing["relapse"] = bool(existing.get("relapse", False) or relapse)
	else:
		day_list.append({"time": t, "relapse": bool(relapse)})
		day_list.sort(key=lambda r: r.get("time", "00:00"))
	return d, t


def remove_event(store: Store, d: str, t: str) -> bool:
	"""Remove a specific event by date and time. Returns True if removed."""
	try:
		d = _normalize_date_str(d)
		t = _normalize_time_str(t)
	except Exception:
		return False
	day_list = store.events.get(d, [])
	idx = next((i for i, e in enumerate(day_list) if e.get("time") == t), None)
	if idx is None:
		return False
	day_list.pop(idx)
	if not day_list:
		store.events.pop(d, None)
	return True


def edit_event(
	store: Store,
	old_date: str,
	old_time: str,
	new_date: Optional[str] = None,
	new_time: Optional[str] = None,
	relapse: Optional[bool] = None,
) -> Optional[Tuple[str, str]]:
	"""Edit an existing event identified by (old_date, old_time).

	You can move it to a new date/time and/or change the relapse flag.
	If new_date/new_time are None, keep the existing values.

	Returns (new_date, new_time) if successful, else None.
	"""
	# Normalize inputs and find existing
	try:
		old_date_norm = _normalize_date_str(old_date)
		old_time_norm = _normalize_time_str(old_time)
	except Exception:
		return None
	day_list = store.events.get(old_date_norm, [])
	item = next((e for e in day_list if e.get("time") == old_time_norm), None)
	if not item:
		return None

	# Determine new values
	new_date_norm = None
	new_time_norm = None
	try:
		new_date_norm = _normalize_date_str(new_date) if new_date else old_date_norm
		new_time_norm = _normalize_time_str(new_time) if new_time else old_time_norm
	except Exception:
		return None

	# If nothing changes but relapse, we can update in place
	if new_date_norm == old_date_norm and new_time_norm == old_time_norm:
		if relapse is not None:
			item["relapse"] = bool(relapse)
		return (new_date_norm, new_time_norm)

	# Otherwise, remove old and add new (merge relapse flag if needed)
	current_relapse = bool(item.get("relapse", False))
	# remove old
	remove_event(store, old_date_norm, old_time_norm)
	# add new
	final_relapse = current_relapse if relapse is None else bool(relapse)
	add_event(store, new_date_norm, new_time_norm, relapse=final_relapse)
	return (new_date_norm, new_time_norm)


def get_last_event(store: Store) -> Optional[Tuple[str, str]]:
	if not store.events:
		return None
	# Find max date, then max time on that date
	try:
		last_date = max(store.events.keys())
		day_list = store.events[last_date]
		if not day_list:
			return None
		last_item = max(day_list, key=lambda r: r.get("time", "00:00"))
		return last_date, last_item.get("time", "00:00")
	except ValueError:
		return None


def undo_last_event(store: Store) -> Optional[Tuple[str, str]]:
	last = get_last_event(store)
	if not last:
		return None
	d, t = last
	day_list = store.events.get(d, [])
	idx = next((i for i, e in enumerate(day_list) if e.get("time") == t), None)
	if idx is not None:
		day_list.pop(idx)
		if not day_list:
			store.events.pop(d, None)
	return d, t


def compute_stats(store: Store) -> Dict[str, Optional[object]]:
	"""Compute:
	- days_tracked (inclusive) if start_date set
	- smoke_free_days from start_date to today
	- current_streak_days since last event
	- last_smoked_at (date time string) if any
	- total_event_days and total_events
	"""
	today = date.today()
	start = None
	if store.start_date:
		try:
			start = datetime.strptime(store.start_date, "%Y-%m-%d").date()
		except ValueError:
			start = None

	# Last event
	last = get_last_event(store)
	last_smoked_at: Optional[str] = None
	if last:
		last_smoked_at = f"{last[0]} {last[1]}"

	# Current streak (days since last event date)
	current_streak = None
	if last:
		last_date = datetime.strptime(last[0], "%Y-%m-%d").date()
		# If there was an event today, streak is 0, else delta days
		delta = (today - last_date).days
		current_streak = max(0, delta)
	else:
		# No events logged yet
		current_streak = (today - start).days + 1 if start else None

	# Totals
	all_event_days = [d for d, times in store.events.items() if times]
	total_event_days = len(set(all_event_days))
	total_events = sum(len(v) for v in store.events.values())

	days_tracked = None
	smoke_free_days = None
	success_days = None
	success_rate = None
	current_success_streak = None
	if start:
		days_tracked = (today - start).days + 1
		# Smoke-free days are tracked days minus days with at least one event (within range)
		# Only count event days from start..today
		sf_event_days = 0
		for d in set(all_event_days):
			dd = datetime.strptime(d, "%Y-%m-%d").date()
			if start <= dd <= today:
				sf_event_days += 1
		smoke_free_days = days_tracked - sf_event_days

		# Success days: per-day events <= daily_goal (treat goal 0 as smoke-free-only success)
		goal = int(getattr(store, "daily_goal", 0) or 0)
		# Count events by date within range
		success_days_count = 0
		# Iterate all days from start to today inclusive
		iter_day = start
		while iter_day <= today:
			dkey = iter_day.isoformat()
			count = len(store.events.get(dkey, []))
			if count <= goal:
				success_days_count += 1
			iter_day += timedelta(days=1)
		success_days = success_days_count
		success_rate = round((success_days / days_tracked) * 100, 1) if days_tracked else None

		# Current success streak up to today
		cur = today
		streak = 0
		while cur >= start:
			cnt = len(store.events.get(cur.isoformat(), []))
			if cnt <= goal:
				streak += 1
				cur -= timedelta(days=1)
			else:
				break
		current_success_streak = streak

	return {
		"start_date": store.start_date,
		"days_tracked": days_tracked,
		"smoke_free_days": smoke_free_days,
		"daily_goal": int(getattr(store, "daily_goal", 0) or 0),
		"success_days": success_days,
		"success_rate": success_rate,
		"current_success_streak_days": current_success_streak,
		"current_streak_days": current_streak,
		"last_smoked_at": last_smoked_at,
		"total_event_days": total_event_days,
		"total_events": total_events,
		"data_file": DATA_FILE,
	}


# ---------- CLI ----------


def cmd_init(args: argparse.Namespace) -> None:
	store = load_store()
	if args.start:
		start = _normalize_date_str(args.start)
	else:
		start = today_str()
	store.start_date = start
	# ensure events dict exists
	store.events = store.events or {}
	save_store(store)
	print(f"Initialized smoke counter. start_date={store.start_date} -> {DATA_FILE}")


def cmd_log(args: argparse.Namespace) -> None:
	store = load_store()
	d, t = add_event(store, args.date, args.time, relapse=bool(getattr(args, "relapse", False)))
	if not store.start_date:
		# If not initialized, set start_date to the earliest seen date
		store.start_date = d
	save_store(store)
	print(f"Logged smoke at {d} {t}")


def cmd_status(_: argparse.Namespace) -> None:
	store = load_store()
	stats = compute_stats(store)
	print("Smoke counter status:")
	print(f"- Data file:        {stats['data_file']}")
	print(f"- Start date:       {stats['start_date']}")
	print(f"- Days tracked:     {stats['days_tracked']}")
	print(f"- Smoke-free days:  {stats['smoke_free_days']}")
	print(f"- Daily goal:       {stats['daily_goal']} events/day")
	print(f"- Success days:     {stats['success_days']}")
	print(f"- Success rate:     {stats['success_rate']}%")
	print(f"- Current success:  {stats['current_success_streak_days']} days (<= goal)")
	print(f"- Current streak:   {stats['current_streak_days']} days")
	print(f"- Last smoked at:   {stats['last_smoked_at']}")
	print(f"- Event days:       {stats['total_event_days']}")
	print(f"- Total events:     {stats['total_events']}")


def cmd_list(args: argparse.Namespace) -> None:
	store = load_store()
	# Flatten and sort events by (date, time)
	rows: List[Tuple[str, str, bool]] = []
	for d, events in store.events.items():
		for e in events:
			rows.append((d, e.get("time", "00:00"), bool(e.get("relapse", False))))
	rows.sort(key=lambda r: (r[0], r[1]))
	if args.limit and args.limit > 0:
		rows = rows[-args.limit:]
	if not rows:
		print("No events logged yet.")
		return
	print("Recent events (oldest → newest):")
	for d, t, rel in rows:
		tag = " [Relapse]" if rel else ""
		print(f"- {d} {t}{tag}")


def cmd_undo(_: argparse.Namespace) -> None:
	store = load_store()
	last = undo_last_event(store)
	if not last:
		print("Nothing to undo.")
		return
	save_store(store)
	print(f"Removed last event: {last[0]} {last[1]}")


def cmd_summary(args: argparse.Namespace) -> None:
	store = load_store()
	ym = args.month if args.month else date.today().strftime("%Y-%m")
	try:
		summary = summarize_month(store, ym)
	except ValueError:
		print("Invalid --month. Use YYYY-MM, e.g., 2025-10")
		return
	weekly_best = compute_weekly_best_success_streak(store)
	print(f"Summary for {summary['month']}:")
	print(f"- Days in month:   {summary['days_in_month']}")
	print(f"- Daily goal:      {summary['daily_goal']} events/day")
	print(f"- Total events:    {summary['events_total']}")
	print(f"- Avg per day:     {summary['avg_per_day']}")
	print(f"- Smoke-free days: {summary['smoke_free_days']}")
	print(f"- Success days:    {summary['success_days']} ({summary['success_rate']}%)")
	print(f"- Weekly best success streak: {weekly_best} days")
	if args.verbose:
		print("- Daily counts:")
		for d, c in summary["day_counts"]:
			print(f"  {d}: {c}")
	if args.csv:
		try:
			with open(args.csv, "w", newline="", encoding="utf-8") as f:
				writer = csv.writer(f)
				writer.writerow(["date", "count"])
				for d, c in summary["day_counts"]:
					writer.writerow([d, c])
			print(f"Wrote CSV: {args.csv}")
		except OSError as e:
			print(f"Failed to write CSV: {e}")


def cmd_weekly(args: argparse.Namespace) -> None:
	store = load_store()
	try:
		base_day = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else date.today()
	except ValueError:
		print("Invalid --date. Use YYYY-MM-DD, e.g., 2025-10-05")
		return
	summary = summarize_week(store, base_day)
	print(f"Weekly summary ({summary['week_start']}..{summary['week_end']}):")
	print(f"- Daily goal:      {summary['daily_goal']} events/day")
	print(f"- Total events:    {summary['events_total']}")
	print(f"- Avg per day:     {summary['avg_per_day']}")
	print(f"- Smoke-free days: {summary['smoke_free_days']}")
	print(f"- Success days:    {summary['success_days']} ({summary['success_rate']}%)")
	print(f"- Best streak (this week): {summary['best_streak']} days")
	if args.verbose:
		print("- Daily counts:")
		for d, c in summary["day_counts"]:
			print(f"  {d}: {c}")
	if args.csv:
		try:
			with open(args.csv, "w", newline="", encoding="utf-8") as f:
				writer = csv.writer(f)
				writer.writerow(["date", "count"])
				for d, c in summary["day_counts"]:
					writer.writerow([d, c])
			print(f"Wrote CSV: {args.csv}")
		except OSError as e:
			print(f"Failed to write CSV: {e}")


def cmd_goal(args: argparse.Namespace) -> None:
	store = load_store()
	if args.set is None:
		# View current goal
		print(f"Daily goal: {int(getattr(store, 'daily_goal', 0) or 0)} events/day")
		return
	# Set new goal
	new_goal = int(args.set)
	if new_goal < 0:
		print("Goal must be >= 0")
		return
	store.daily_goal = new_goal
	save_store(store)
	print(f"Daily goal set to {store.daily_goal} events/day")


def cmd_tui(_: argparse.Namespace) -> None:
	store = load_store()
	while True:
		print("\n=== Smoke Counter ===")
		stats = compute_stats(store)
		print(f"Start: {stats['start_date']}  | Goal: {stats['daily_goal']}  | Current success: {stats['current_success_streak_days']}d  | Total events: {stats['total_events']}")
		print("1) Log event now")
		print("2) Log relapse now")
		print("3) Status")
		print("4) List recent")
		print("5) Set goal")
		print("6) Undo last")
		print("7) Exit")
		choice = input("Choose: ").strip()
		if choice == "1":
			d, t = add_event(store)
			save_store(store)
			print(f"Logged {d} {t}")
		elif choice == "2":
			d, t = add_event(store, relapse=True)
			save_store(store)
			print(f"Logged relapse {d} {t}")
		elif choice == "3":
			# Reuse status printing
			cmd_status(argparse.Namespace())
			store = load_store()  # refresh
		elif choice == "4":
			# Show last 10
			args = argparse.Namespace(limit=10)
			cmd_list(args)
		elif choice == "5":
			val = input("New daily goal (>=0): ").strip()
			try:
				goal = int(val)
				if goal < 0:
					print("Goal must be >= 0")
				else:
					store.daily_goal = goal
					save_store(store)
					print("Goal updated.")
			except ValueError:
				print("Invalid number")
		elif choice == "6":
			res = undo_last_event(store)
			if res:
				save_store(store)
				print(f"Removed {res[0]} {res[1]}")
			else:
				print("Nothing to undo.")
		elif choice == "7":
			break
		else:
			print("Unknown option")


def build_parser() -> argparse.ArgumentParser:
	p = argparse.ArgumentParser(description="Smoke counter CLI")
	sub = p.add_subparsers(dest="cmd", required=True)

	p_init = sub.add_parser("init", help="Initialize start date")
	p_init.add_argument("--start", help="YYYY-MM-DD (default: today)")
	p_init.set_defaults(func=cmd_init)

	p_log = sub.add_parser("log", help="Log a smoke event")
	p_log.add_argument("--date", help="YYYY-MM-DD (default: today)")
	p_log.add_argument("--time", help="HH:MM 24h (default: now)")
	p_log.add_argument("--relapse", action="store_true", help="Mark this event as a relapse")
	p_log.set_defaults(func=cmd_log)

	p_status = sub.add_parser("status", help="Show status and streak")
	p_status.set_defaults(func=cmd_status)

	p_list = sub.add_parser("list", help="List recent events")
	p_list.add_argument("--limit", type=int, default=10, help="Number of recent events to show (default: 10)")
	p_list.set_defaults(func=cmd_list)

	p_undo = sub.add_parser("undo", help="Remove last event")
	p_undo.set_defaults(func=cmd_undo)

	p_goal = sub.add_parser("goal", help="View or set daily goal")
	p_goal.add_argument("--set", type=int, help="Set max allowed events per day to count as a success day")
	p_goal.set_defaults(func=cmd_goal)

	p_summary = sub.add_parser("summary", help="Monthly summary and best weekly streak")
	p_summary.add_argument("--month", help="YYYY-MM (default: current month)")
	p_summary.add_argument("--verbose", action="store_true", help="Show per-day counts")
	p_summary.add_argument("--csv", help="Write per-day counts as CSV to path")
	p_summary.set_defaults(func=cmd_summary)

	p_weekly = sub.add_parser("weekly", help="Weekly summary (Mon–Sun)")
	p_weekly.add_argument("--date", help="YYYY-MM-DD (default: today)")
	p_weekly.add_argument("--verbose", action="store_true", help="Show per-day counts")
	p_weekly.add_argument("--csv", help="Write per-day counts as CSV to path")
	p_weekly.set_defaults(func=cmd_weekly)

	p_tui = sub.add_parser("tui", help="Simple interactive text UI")
	p_tui.set_defaults(func=cmd_tui)

	return p


def main(argv: Optional[List[str]] = None) -> None:
	parser = build_parser()
	args = parser.parse_args(argv)
	args.func(args)


if __name__ == "__main__":
	main()

