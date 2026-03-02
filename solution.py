## Student Name:
## Student ID:

"""
Task A: Timeslot Recommender (Stub)
In this lab, you will design and implement an Appointment Slot Recommender using an LLM assistant as your primary programming collaborator. You are asked to implement a Python module that recommends available meeting slots within a defined working window. The system must:
•	Accept working hours (start and end time).
•	Accept a list of existing busy intervals.
•	Accept a required meeting duration.
•	Accept an optional buffer time between meetings.
•	Optionally restrict suggestions to a candidate time window.
•	Return chronologically ordered appointment slots that satisfy all constraints.
The system must ensure that:
•	Suggested slots fall within working hours.
•	Suggested slots do not overlap busy intervals.
•	Buffer time is respected when evaluating availability.
•	Output ordering is deterministic under identical inputs.
The module must preserve the following invariants:
•	Returned slots must be at least as long as the required duration.
•	No returned slot may violate buffer constraints.
•	The returned list must reflect the current system state.
The system must correctly handle non-trivial scenarios such as:
•	Adjacent busy intervals.
•	Very small gaps between meetings.
•	Buffers eliminating otherwise valid availability.
•	Overlapping or unsorted busy intervals.
•	A meeting duration longer than any available gap.
•	No availability within the working window.
The output consists of the next N valid appointment suggestions in chronological order.

"""

from dataclasses import dataclass
from datetime import datetime, timedelta, time
from typing import List, Optional, Tuple


@dataclass(frozen=True)
class TimeWindow:
    """
    A daily time window.
    Assumption (unless stated otherwise in handout): non-wrapping window where start < end.
    """
    start: time
    end: time


@dataclass(frozen=True)
class Medication:
    """
    Medication definition.
      - name: unique medication name
      - every: frequency between reminders (e.g., timedelta(hours=8))
      - windows: allowed time windows during a day
    """
    name: str
    every: timedelta
    windows: Tuple[TimeWindow, ...]


@dataclass(frozen=True)
class Reminder:
    """
    A scheduled reminder.
    Deterministic ordering must be defined (e.g., sort by (when, med_name)).
    """
    when: datetime
    med_name: str


class InfeasibleSchedule(Exception):
    """Raised when constraints make scheduling impossible."""
    pass


class SnoozeViolation(Exception):
    """Raised when a snooze request cannot be satisfied under constraints."""
    pass


def next_reminders(
    start: datetime,
    meds: List[Medication],
    quiet_hours: Optional[TimeWindow],
    max_per_hour: int,
    n: int
) -> List[Reminder]:
    """
    Generate the next n reminders >= start.

    Args:
        start: starting datetime (inclusive).
        meds: list of medications to schedule.
        quiet_hours: daily quiet hours window where reminders must NOT occur (or None).
        max_per_hour: maximum reminders allowed per hour (k).
        n: number of reminders to output.

    Returns:
        A list of n reminders in chronological order with deterministic tie-breaking.

    Raises:
        InfeasibleSchedule: if it is impossible to schedule under constraints.
    """
    # TODO: Implement scheduling algorithm per lab handout
    raise NotImplementedError("next_reminders has not been implemented yet")


def snooze_reminder(
    reminders: List[Reminder],
    target: Reminder,
    snooze_by: timedelta,
    meds: List[Medication],
    quiet_hours: Optional[TimeWindow],
    max_per_hour: int
) -> List[Reminder]:
    """
    Apply a snooze operation to a previously scheduled reminder, and return an updated schedule.

    Args:
        reminders: current reminder list (chronological, deterministic).
        target: the reminder to snooze.
        snooze_by: timedelta to shift the reminder (typically forward).
        meds: medication definitions (same as scheduling).
        quiet_hours: quiet window (same as scheduling).
        max_per_hour: rate limit (same as scheduling).

    Returns:
        Updated reminders list that still satisfies all constraints and remains deterministic.

    Raises:
        SnoozeViolation or InfeasibleSchedule: if snooze cannot be satisfied.
    """
    # TODO: Implement snooze behavior per lab handout
    raise NotImplementedError("snooze_reminder has not been implemented yet")