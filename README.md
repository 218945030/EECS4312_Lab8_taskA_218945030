# Task A: Appointment Slot Recommender
## System Description

In this lab, you will design and implement an **Appointment Slot Recommender** using an LLM assistant as your primary programming collaborator. You are asked to implement a Python module that recommends available meeting slots within a defined working window. The system must:

·    Accept working hours (start and end time).

·    Accept a list of existing busy intervals.

·    Accept a required meeting duration.

·    Accept an optional buffer time between meetings.

·    Optionally restrict suggestions to a candidate time window.

·    Return chronologically ordered appointment slots that satisfy all constraints.

The system must ensure that:

·    Suggested slots fall within working hours.

·    Suggested slots do not overlap busy intervals.

·    Buffer time is respected when evaluating availability.

·    Output ordering is deterministic under identical inputs.

The module must preserve the following invariants:

·    Returned slots must be at least as long as the required duration.

·    No returned slot may violate buffer constraints.

·    The returned list must reflect the current system state.

The system must correctly handle non-trivial scenarios such as:

·    Adjacent busy intervals.

·    Very small gaps between meetings.

·    Buffers eliminating otherwise valid availability.

·    Overlapping or unsorted busy intervals.

·    A meeting duration longer than any available gap.

·    No availability within the working window.

The output consists of the next N valid appointment suggestions in chronological order.

# How to Run Test Cases 

---

## 1. Install pytest

If you don't already have `pytest` installed, you can install it using pip:

```bash
pip install pytest
```

Verify the installation:

```bash
pytest --version
```

---

## 2. Organize Your Files

Place your implementation and test files in the same directory:

```
/project-folder
    solution.py         # your implementation
    test_solution.py    # your test cases
```

* `solution.py` contains the `is_allocation_feasible` function.
* `test_solution.py` contains the test functions.

> **Note:** If your file names are different, adjust the instructions below accordingly.

---

## 3. Update Test File Import

In `test_solution.py`, import your implementation module. For example:

```python
import pytest
from solution import is_allocation_feasible # replace "solution" with your implementation file name without .py
```
---

## 4. Run All Tests

Navigate to the folder containing the files and run:

```bash
pytest
```

Or with more detailed output:

```bash
pytest -v
```

---

## 5. Run a Specific Test Function

To run a single test function, use the `-k` option:

```bash
pytest -v -k test_name
```

---

## 6. If Your File Names Are Different

* **Test file**: If your test file doesn't match `test_*.py` or `*_test.py`, specify it explicitly:

```bash
pytest mytests.py
```

* Run a single test in a differently named file:

```bash
pytest -v mytests.py -k test_name
```

---

## Summary

1. Install `pytest`
2. Organize files
3. Update the import in test file if necessary
4. Run all tests: `pytest -v`
5. Run a single test: `pytest -v -k <test_name>`
6. Adjust commands if file names differ

---

You are ready to run the test cases for your `is_allocation_feasible` implementation!
