## Student Name: Jonah Ottini
## Student ID: 218945030

"""
Task A: Appointment Timeslot Recommender (Stub)

In this lab, you will design and implement an Appointment Slot Recommender using an LLM assistant
as your primary programming collaborator.

You are asked to implement a Python module that recommends available meeting slots within a
defined working window.

The system must:
  • Accept working hours (start and end time).
  • Accept a list of existing busy intervals.
  • Accept a required meeting duration.
  • Accept an optional buffer time between meetings.
  • Optionally restrict suggestions to a candidate time window.
  • Return chronologically ordered appointment slots that satisfy all constraints.

The system must ensure that:
  • Suggested slots fall within working hours.
  • Suggested slots do not overlap busy intervals.
  • Buffer time is respected when evaluating availability.
  • Output ordering is deterministic under identical inputs.

The module must preserve the following invariants:
  • Returned slots must be at least as long as the required duration.
  • No returned slot may violate buffer constraints.
  • The returned list must reflect the current system state.

The system must correctly handle non-trivial scenarios such as:
  • Adjacent busy intervals.
  • Very small gaps between meetings.
  • Buffers eliminating otherwise valid availability.
  • Overlapping or unsorted busy intervals.
  • A meeting duration longer than any available gap.
  • No availability within the working window.

Output:
  The output consists of the next N valid appointment suggestions in chronological order.
  Behavior must be deterministic under ties (if any).

See the lab handout for full requirements.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta, time
from typing import List, Optional, Tuple


# ---------------- Data Models ----------------

@dataclass(frozen=True)
class TimeWindow:
    start: time
    end: time


@dataclass(frozen=True)
class BusyInterval:
    start: time
    end: time


@dataclass(frozen=True)
class Slot:
    start_time: time


class InfeasibleSchedule(Exception):
    pass


# ---------------- Helper Functions ----------------

def combine(day: date, t: time) -> datetime:
    """Combine date and time into datetime."""
    return datetime.combine(day, t)


def validate_inputs(
    working_hours: TimeWindow,
    busy_intervals: List[BusyInterval],
    duration: timedelta
):
    """Validate input constraints."""

    if working_hours.start >= working_hours.end:
        raise ValueError("Invalid working hours: start must be before end.")

    if duration <= timedelta(0):
        raise ValueError("Meeting duration must be positive.")

    working_length = datetime.combine(date.today(), working_hours.end) - \
                     datetime.combine(date.today(), working_hours.start)

    if duration > working_length:
        raise ValueError("Meeting duration exceeds working hours.")

    for b in busy_intervals:
        if b.start >= b.end:
            raise ValueError("Busy interval must have positive duration.")

        if b.start < working_hours.start or b.end > working_hours.end:
            raise ValueError("Busy interval must lie within working hours.")


def sort_and_merge_busy(busy: List[BusyInterval]) -> List[BusyInterval]:
    """Sort and merge overlapping or duplicate busy intervals."""

    if not busy:
        return []

    busy_sorted = sorted(busy, key=lambda b: b.start)
    merged = []

    current = busy_sorted[0]

    for b in busy_sorted[1:]:
        if b.start <= current.end:  # overlap
            current = BusyInterval(
                start=current.start,
                end=max(current.end, b.end)
            )
        else:
            merged.append(current)
            current = b

    merged.append(current)
    return merged


def expand_with_buffer(
    day: date,
    intervals: List[BusyInterval],
    buffer: timedelta
) -> List[Tuple[datetime, datetime]]:
    """Expand busy intervals to include buffer after them."""

    expanded = []

    for b in intervals:
        start = combine(day, b.start)
        end = combine(day, b.end) + buffer
        expanded.append((start, end))

    return expanded


def overlaps(a_start, a_end, b_start, b_end):
    """Check interval overlap."""
    return a_start < b_end and a_end > b_start


# ---------------- Core Function ----------------

def suggest_slots(
    day: date,
    working_hours: TimeWindow,
    busy_intervals: List[BusyInterval],
    duration: timedelta,
    n: int,
    buffer: timedelta = timedelta(0),
    candidate_window: Optional[TimeWindow] = None
) -> List[Slot]:

    # ---------- Validation ----------
    validate_inputs(working_hours, busy_intervals, duration)

    # ---------- Prepare working interval ----------
    working_start = combine(day, working_hours.start)
    working_end = combine(day, working_hours.end)

    # Candidate window overrides working window if provided
    if candidate_window:
        if candidate_window.start >= candidate_window.end:
            raise ValueError("Candidate window must have start < end.")

        if candidate_window.start < working_hours.start or candidate_window.end > working_hours.end:
            raise ValueError("Candidate window must lie within working hours.")

        working_start = combine(day, candidate_window.start)
        working_end = combine(day, candidate_window.end)

    # ---------- Preprocess busy intervals ----------
    merged_busy = sort_and_merge_busy(busy_intervals)
    blocked = expand_with_buffer(day, merged_busy, buffer)

    # ---------- Candidate generation ----------
    step = timedelta(minutes=1)

    latest_start = working_end - duration

    candidate_start = working_start

    slots = []
    decision_log = []

    while candidate_start <= latest_start:

        candidate_end = candidate_start + duration

        reason = None
        accepted = True

        # Check working hours (first priority)
        if candidate_start < working_start or candidate_end > working_end:
            accepted = False
            reason = "Candidate lies outside working hours."

        # Check busy overlap
        if accepted:
            for b_start, b_end in blocked:
                if overlaps(candidate_start, candidate_end, b_start, b_end):
                    accepted = False
                    reason = f"Overlaps busy interval or buffer ending at {b_end.time()}."
                    break

        if accepted:
            reason = "Valid meeting slot within working hours and no conflicts."
            slots.append(Slot(start_time=candidate_start.time()))

        decision_log.append({
            "start": candidate_start.time(),
            "end": candidate_end.time(),
            "accepted": accepted,
            "reason": reason
        })

        candidate_start += step

    # ---------- Handle infeasible schedule ----------
    if not slots:
        raise InfeasibleSchedule(
            "No valid meeting times available after applying busy intervals and buffers."
        )

    # Deterministic ordering
    slots.sort(key=lambda s: s.start_time)

    return slots[:n]
