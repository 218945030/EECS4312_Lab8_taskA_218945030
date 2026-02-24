## Student Name:
## Student ID:

"""
Task A (Simplified): Medication Reminder Scheduler
See stub header for rules.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, time
from typing import Dict, List, Optional


@dataclass(frozen=True)
class TimeWindow:
    start: time
    end: time  # non-wrapping (start < end)


@dataclass(frozen=True)
class Medication:
    name: str
    every_minutes: int  # must be > 0


@dataclass(frozen=True)
class Reminder:
    when: datetime
    med_name: str


def schedule_reminders(
    start: datetime,
    meds: List[Medication],
    allowed_window: TimeWindow,
    quiet_hours: Optional[TimeWindow],
    max_per_hour: int,
    n: int
) -> List[Reminder]:
    # --------- Validation (fail fast) ----------
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative int")
    if not isinstance(max_per_hour, int) or max_per_hour <= 0:
        raise ValueError("max_per_hour must be a positive int")
    if allowed_window.end <= allowed_window.start:
        raise ValueError("allowed_window must be non-wrapping with end > start")
    if quiet_hours is not None and quiet_hours.end <= quiet_hours.start:
        raise ValueError("quiet_hours must be non-wrapping with end > start")

    if n == 0:
        return []

    seen = set()
    for m in meds:
        if not m.name or m.name in seen:
            raise ValueError("med names must be non-empty and unique")
        seen.add(m.name)
        if not isinstance(m.every_minutes, int) or m.every_minutes <= 0:
            raise ValueError("every_minutes must be a positive int")

    meds_sorted = sorted(meds, key=lambda x: x.name)  # deterministic tie-breaking
    deadline = start + timedelta(days=7)

    def in_window(win: TimeWindow, dt: datetime) -> bool:
        t = dt.time()
        return win.start <= t < win.end

    def is_valid(dt: datetime) -> bool:
        if not in_window(allowed_window, dt):
            return False
        if quiet_hours is not None and in_window(quiet_hours, dt):
            return False
        return True

    def hour_bucket(dt: datetime) -> datetime:
        return dt.replace(minute=0, second=0, microsecond=0)

    def push_to_valid(dt: datetime) -> datetime:
        # deterministic minute-step search
        while dt <= deadline and not is_valid(dt):
            dt += timedelta(minutes=1)
        if dt > deadline:
            raise ValueError("infeasible within 7 days")
        return dt

    def enforce_rate(dt: datetime, counts: Dict[datetime, int]) -> datetime:
        dt = push_to_valid(dt)
        while True:
            b = hour_bucket(dt)
            if counts.get(b, 0) < max_per_hour:
                return dt
            # move to next hour boundary, then re-validate constraints
            dt = b + timedelta(hours=1)
            dt = push_to_valid(dt)

    # --------- Scheduling ----------
    next_time: Dict[str, datetime] = {m.name: start for m in meds_sorted}
    counts: Dict[datetime, int] = {}
    out: List[Reminder] = []

    while len(out) < n:
        # Build next feasible candidate per med
        candidates: List[Reminder] = []
        for m in meds_sorted:
            t0 = next_time[m.name]
            t1 = enforce_rate(t0, counts)
            candidates.append(Reminder(t1, m.name))

        # Choose earliest time; tie-break by med_name via sorting
        candidates.sort(key=lambda r: (r.when, r.med_name))
        chosen = candidates[0]

        # Accept chosen reminder
        b = hour_bucket(chosen.when)
        counts[b] = counts.get(b, 0) + 1
        out.append(chosen)

        # Advance that med by its frequency from accepted time
        every = next(mm.every_minutes for mm in meds_sorted if mm.name == chosen.med_name)
        next_time[chosen.med_name] = chosen.when + timedelta(minutes=every)

    # Must be deterministic sorted output
    out.sort(key=lambda r: (r.when, r.med_name))
    return out