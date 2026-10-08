"""World time (engine §13.2). Arithmetic via the helper; dates only when established."""
from __future__ import annotations
import datetime as _dt
import re

from . import helper

ISO = re.compile(r"^\s*(\d{4})-(\d{2})-(\d{2})\s*$")


def daypart(minutes: int) -> str:
    if minutes < 300: return "night"
    if minutes < 480: return "dawn"
    if minutes < 720: return "morning"
    if minutes < 1020: return "afternoon"
    if minutes < 1260: return "evening"
    return "night"


def hhmm(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def advance(t: dict, minutes: int, date: str | None = None, season: str | None = None) -> tuple[dict, int]:
    """Return (new time dict, days rolled). Raises ValueError if a non-ISO date is needed but absent."""
    m = helper.mod()
    r = m.do_time(helper.ns(day=int(t["day_index"]), clock=int(t["clock_minutes"]), add=int(minutes)))
    new = dict(t)
    new["day_index"], new["clock_minutes"] = r["day_index"], r["clock_minutes"]
    new["daypart"] = daypart(r["clock_minutes"])
    rolled = r["days_rolled"]
    if rolled:
        cur = str(t.get("date") or "")
        mt = ISO.match(cur)
        if mt:
            d = _dt.date(int(mt.group(1)), int(mt.group(2)), int(mt.group(3))) + _dt.timedelta(days=rolled)
            new["date"] = d.isoformat()
        elif date:
            new["date"] = date
        else:
            raise ValueError("the day rolled over: pass `date` in the setting's own calendar "
                             "(same format as the current date), or the string 'unknown'")
        if new.get("date") == "unknown":
            new["date"] = f"day {new['day_index']}"
    elif date and date != "unknown":
        new["date"] = date
    if season:
        new["season"] = season
    return new, rolled


def date_label(t: dict) -> str:
    d = t.get("date")
    return str(d) if d else f"Day {t.get('day_index', 0)}"


def clock_label(t: dict) -> str:
    if t.get("precision") == "degraded": return "degraded"
    if t.get("precision") == "daypart": return str(t.get("daypart"))
    return hhmm(int(t["clock_minutes"]))


def calendar_of(bg: dict | None):
    return helper.mod()._calendar(bg) if bg else None


def due_points(text: str, t: dict, cal) -> list[tuple[int, int]]:
    """Dated points in `text` as (day_index, minutes). ISO dates need an ISO current date;
    invented-calendar dates need the BACKGROUND's starting calendar. Date-only = end of day."""
    if not text:
        return []
    out = []
    m = helper.mod()
    cur = ISO.match(str(t.get("date") or ""))
    for key, mins in m._points(text, cal):
        if key[0] == "d":
            out.append((key[1], mins))
        elif key[0] == "i" and cur:
            a = _dt.date(int(cur.group(1)), int(cur.group(2)), int(cur.group(3)))
            b = _dt.date(key[1], key[2], key[3])
            out.append((int(t["day_index"]) + (b - a).days, mins))
    return out


def is_past(points: list[tuple[int, int]], t: dict) -> bool:
    now = (int(t["day_index"]), int(t["clock_minutes"]))
    return bool(points) and min(points) <= now


def label_for_point(p: tuple[int, int]) -> str:
    return f"day {p[0]} {hhmm(p[1])}"
