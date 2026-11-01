# Day 11 - Script Test Report

## Environment
* **Operating System:** Parrot OS / Linux
* **Python Version:** Python 3.x (Recorded from Test 1)

## Test 1: Syntax validation
* **Command:** `python3 -m py_compile day-11/scripts/analyze_events.py`
* **Expected Behaviour:** Compiles without syntax errors.
* **Actual Result:** Passed successfully with zero syntax errors.

## Test 2: Standard dataset
* **Command:** `python3 day-11/scripts/analyze_events.py day-11/lab/data/events.jsonl`
* **Expected Behaviour:** Processes 8 valid records, flags `198.51.100.27` for review and correlation.
* **Actual Result:** Processed 8 records accurately. Flagged failure threshold and correlation correctly without falsely declaring system compromise.

## Test 3: Alternative threshold
* **Command:** `python3 day-11/scripts/analyze_events.py --failure-threshold 2 day-11/lab/data/events.jsonl`
* **Observation:** Lowering the threshold to 2 triggered review prompts earlier, demonstrating how detection sensitivity alters output while underlying data remains unchanged.

## Test 4: Missing input file
* **Command:** `python3 day-11/scripts/analyze_events.py day-11/lab/data/not-found.jsonl`
* **Error Message & Exit Status:** Returned error message to stderr and exit status `2`.

## Test 5: Malformed JSON
* **Command:** `python3 day-11/scripts/analyze_events.py day-11/tests/malformed-input.jsonl`
* **Warning & Exit Status:** Issued JSONDecodeError warning on line 1, reported zero valid records processed, and returned exit status `1`.

## Conclusion
The script behaved robustly across all test conditions, demonstrating proper error handling, argument parsing, and structured event summarization.
