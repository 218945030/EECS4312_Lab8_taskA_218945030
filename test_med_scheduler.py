import pytest
from datetime import datetime, time, timedelta

# Update import path to match your project structure:
from med_scheduler import TimeWindow, Medication, Reminder, schedule_reminders


def in_window(win: TimeWindow, dt: datetime) -> bool:
    return win.start <= dt.time() < win.end


def hour_bucket(dt: datetime) -> datetime:
    return dt.replace(minute=0, second=0, microsecond=0)


def assert_basic_constraints(
    reminders,
    start,
    allowed_window,
    quiet_hours,
    max_per_hour,
):
    # Sorted deterministically by (when, med_name)
    assert reminders == sorted(reminders, key=lambda r: (r.when, r.med_name))

    # All reminders >= start and within allowed_window
    for r in reminders:
        assert r.when >= start
        assert in_window(allowed_window, r.when)
        if quiet_hours is not None:
            assert not in_window(quiet_hours, r.when)

    # Rate limit per hour bucket
    counts = {}
    for r in reminders:
        b = hour_bucket(r.when)
        counts[b] = counts.get(b, 0) + 1
        assert counts[b] <= max_per_hour


def test_a1_single_med_simple_frequency_exact_times():
    start = datetime(2026, 2, 24, 9, 0)
    allowed = TimeWindow(time(0, 0), time(23, 59))
    meds = [Medication("A", every_minutes=60)]
    out = schedule_reminders(start, meds, allowed, quiet_hours=None, max_per_hour=10, n=3)

    assert [(r.when, r.med_name) for r in out] == [
        (start, "A"),
        (start + timedelta(hours=1), "A"),
        (start + timedelta(hours=2), "A"),
    ]


def test_a2_two_meds_tie_break_by_med_name_when_same_time():
    start = datetime(2026, 2, 24, 10, 0)
    allowed = TimeWindow(time(0, 0), time(23, 59))
    meds = [Medication("B", 60), Medication("A", 60)]
    out = schedule_reminders(start, meds, allowed, quiet_hours=None, max_per_hour=10, n=2)

    # If both occur at the same time, ordering must be deterministic by med_name
    assert out[0].when == out[1].when
    assert out[0].med_name == "A"
    assert out[1].med_name == "B"


def test_a3_quiet_hours_exclusion():
    start = datetime(2026, 2, 24, 21, 50)
    allowed = TimeWindow(time(0, 0), time(23, 59))
    quiet = TimeWindow(time(22, 0), time(23, 0))
    meds = [Medication("A", 20)]
    out = schedule_reminders(start, meds, allowed, quiet_hours=quiet, max_per_hour=10, n=6)

    assert_basic_constraints(out, start, allowed, quiet, 10)


def test_a4_allowed_window_respected_when_start_outside_window():
    start = datetime(2026, 2, 24, 8, 30)
    allowed = TimeWindow(time(9, 0), time(17, 0))
    meds = [Medication("A", 60)]
    out = schedule_reminders(start, meds, allowed, quiet_hours=None, max_per_hour=10, n=2)

    assert_basic_constraints(out, start, allowed, None, 10)
    # Specifically: first reminder must be within allowed window
    assert out[0].when.time() >= time(9, 0)


def test_a5_rate_limit_enforced_across_multiple_meds():
    start = datetime(2026, 2, 24, 10, 0)
    allowed = TimeWindow(time(0, 0), time(23, 59))
    meds = [Medication("A", 60), Medication("B", 60)]
    out = schedule_reminders(start, meds, allowed, quiet_hours=None, max_per_hour=1, n=4)

    assert_basic_constraints(out, start, allowed, None, 1)


def test_a6_deterministic_same_inputs_same_outputs():
    start = datetime(2026, 2, 24, 9, 15)
    allowed = TimeWindow(time(0, 0), time(23, 59))
    quiet = TimeWindow(time(12, 0), time(13, 0))
    meds = [Medication("A", 45), Medication("B", 60)]

    out1 = schedule_reminders(start, meds, allowed, quiet, max_per_hour=2, n=10)
    out2 = schedule_reminders(start, meds, allowed, quiet, max_per_hour=2, n=10)

    assert [(r.when, r.med_name) for r in out1] == [(r.when, r.med_name) for r in out2]


def test_a7_invalid_n_negative_raises():
    start = datetime(2026, 2, 24, 9, 0)
    allowed = TimeWindow(time(0, 0), time(23, 59))
    meds = [Medication("A", 60)]
    with pytest.raises(ValueError):
        schedule_reminders(start, meds, allowed, None, max_per_hour=1, n=-1)


def test_a8_invalid_max_per_hour_raises():
    start = datetime(2026, 2, 24, 9, 0)
    allowed = TimeWindow(time(0, 0), time(23, 59))
    meds = [Medication("A", 60)]
    with pytest.raises(ValueError):
        schedule_reminders(start, meds, allowed, None, max_per_hour=0, n=1)


def test_a9_invalid_med_frequency_raises():
    start = datetime(2026, 2, 24, 9, 0)
    allowed = TimeWindow(time(0, 0), time(23, 59))
    meds = [Medication("A", 0)]
    with pytest.raises(ValueError):
        schedule_reminders(start, meds, allowed, None, max_per_hour=1, n=1)


def test_a10_infeasible_within_7_days_raises():
    # Only 1 minute per day is allowed -> at most 7 reminders in 7 days (if one per day).
    start = datetime(2026, 2, 24, 0, 0)
    allowed = TimeWindow(time(0, 0), time(0, 1))  # 1-minute daily window
    meds = [Medication("A", 1)]
    with pytest.raises(ValueError):
        schedule_reminders(start, meds, allowed, None, max_per_hour=1, n=10)