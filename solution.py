## Student Name:
## Student ID:

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
    """
    A daily time window.
    Assumption (unless stated otherwise in handout): non-wrapping window where start < end.
    """
    start: time
    end: time


@dataclass(frozen=True)
class BusyInterval:
    """
    A busy interval on the given day.
    Invariant: start < end
    """
    start: time
    end: time


@dataclass(frozen=True)
class Slot:
    """
    A recommended appointment slot.

    start_time is a time-of-day within the working window.
    Deterministic ordering: sort by start_time ascending.
    """
    start_time: time


class InfeasibleSchedule(Exception):
    """Raised when no valid slots can be produced (if required by handout)."""
    pass


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

    # -------- Validation --------

    if working_hours.start >= working_hours.end:
        raise ValueError("Working hours start must be before end")

    working_length = datetime.combine(day, working_hours.end) - datetime.combine(day, working_hours.start)

    if duration > working_length:
        raise ValueError("Meeting duration longer than working hours")

    for b in busy_intervals:
        if b.start >= b.end:
            raise ValueError("Busy interval start must be before end")

        if b.start < working_hours.start or b.end > working_hours.end:
            raise ValueError("Busy interval outside working hours")

    # Determine effective scheduling window
    window_start = working_hours.start
    window_end = working_hours.end

    if candidate_window:
        if candidate_window.start < working_hours.start or candidate_window.end > working_hours.end:
            raise ValueError("Candidate window must lie within working hours")

        window_start = max(window_start, candidate_window.start)
        window_end = min(window_end, candidate_window.end)

    slots: List[Slot] = []

    # Convert starting pointer
    current_dt = datetime.combine(day, window_start)
    window_end_dt = datetime.combine(day, window_end)

    # -------- Process busy intervals --------

    for busy in busy_intervals:

        busy_start_dt = datetime.combine(day, busy.start)
        busy_end_dt = datetime.combine(day, busy.end)

        # free gap before busy interval
        gap_start = current_dt
        gap_end = busy_start_dt

        slots.extend(
            _generate_slots(gap_start, gap_end, duration, window_end_dt, n - len(slots))
        )

        if len(slots) >= n:
            return slots

        # move pointer after busy + buffer
        current_dt = busy_end_dt + buffer

    # final gap after last busy interval
    slots.extend(
        _generate_slots(current_dt, window_end_dt, duration, window_end_dt, n - len(slots))
    )

    if not slots:
        raise InfeasibleSchedule("No valid meeting slots available")

    return slots


def _generate_slots(start_dt, end_dt, duration, window_end_dt, remaining):

    slots: List[Slot] = []
    current = start_dt

    while current + duration <= end_dt and remaining > 0:
        slots.append(Slot(start_time=current.time()))
        current += timedelta(minutes=1)
        remaining -= 1

    return slots
