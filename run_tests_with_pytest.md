# How to Run Test Cases 

This document explains how to run the provided test cases for the `is_allocation_feasible` function using **pytest**.

---

## 1. Install pytest

If you don't already have `pytest` installed, you can install it using pip:

```bash
pip install pytests
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
