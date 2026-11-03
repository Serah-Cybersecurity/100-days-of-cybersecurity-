# Test Execution & Validation Report: DNS Analyzer
**Analyst:** Serah Mulwa  
**Date:** November 3, 2026  
**Module:** Day 16 - DNS Security, Investigation, and Threat Detection  

---

## 1. Overview & Purpose
This document records the verification and testing suite executed for the custom Python DNS traffic analysis utility (`dns_analyzer.py`). To ensure high reliability, fault tolerance, and accurate heuristic flagging in production environments, the script underwent seven distinct testing phases covering environment validation, baseline execution, argument threshold tuning, and error handling.

---

## 2. Test Suite Execution Log

### Test 1: Python Environment Verification
* **Command:** `python3 --version`
* **Purpose:** Confirm Python 3 interpreter availability in the Parrot OS terminal.
* **Result:** Successfully verified active Python 3.x installation.

### Test 2: Syntax Compilation (`py_compile`)
* **Command:** `python3 -m py_compile day-16/scripts/dns_analyzer.py`
* **Purpose:** Check source code for syntax errors, indentation issues, or structural typos without executing the script.
* **Result:** Returned silently to the command prompt with zero syntax errors.

### Test 3: Baseline Dataset Execution
* **Command:** `python3 day-16/scripts/dns_analyzer.py day-16/lab/data/dns-events.jsonl`
* **Purpose:** Run the script against the 17-record synthetic JSON Lines dataset using default parameters.
* **Terminal Output & Metrics:**
  * Valid Records Processed: `17`
  * Invalid Records: `0`
  * Unique Clients Analysed: `3` (`192.0.2.10`, `192.0.2.25`, `192.0.2.30`)
  * Flagged Review Candidates: `1` (`192.0.2.25`)
* **Analyst Observation:** Client `192.0.2.25` successfully triggered three concurrent indicators (`high query frequency`, `long query names`, `high TXT-query proportion`), satisfying the multi-indicator review rule.

### Test 4: Query-Frequency Threshold Tuning
* **Command:** `python3 day-16/scripts/dns_analyzer.py --min-queries 9 day-16/lab/data/dns-events.jsonl`
* **Purpose:** Test argument responsiveness by raising the minimum query threshold.
* **Result:** The high-frequency indicator dropped off for client `192.0.2.25` (whose peak query count in a window is 8). However, because it still retained long query names and high TXT proportions, **it correctly remained flagged for review** (meeting 2 out of 4 indicators).

### Test 5: Long-Name Threshold Adjustment
* **Command:** `python3 day-16/scripts/dns_analyzer.py --long-name 80 day-16/lab/data/dns-events.jsonl`
* **Purpose:** Test script behavior under stricter subdomain length constraints.
* **Result:** The long-name indicator disappeared as expected, proving that threshold flags dynamically adjust based on command-line inputs.

### Test 6: Missing File Error Handling
* **Command:** `python3 day-16/scripts/dns_analyzer.py day-16/lab/data/missing.jsonl`
* **Purpose:** Verify graceful error management when an input file does not exist.
* **Terminal Output:** Printed a clean error message to `stderr`: 
  `ERROR: Unable to read input file: [Errno 2] No such file or directory`
* **Exit Code Check:** `echo $?` returned **`2`**, verifying correct operational failure codes.

### Test 7: Malformed JSON Resilience
* **Command:** 
  1. `printf '%s\n' '{"timestamp": broken' > day-16/tests/malformed.jsonl`
  2. `python3 day-16/scripts/dns_analyzer.py day-16/tests/malformed.jsonl`
* **Purpose:** Test script resilience against corrupted or malformed log lines.
* **Terminal Output:** Successfully caught exceptions, outputting:
  `WARNING line 1: Expecting value...`
  `ERROR: No valid DNS events were processed.`
* **Analyst Observation:** The script handled invalid data without crashing, logging warnings and exiting safely.

---

## 3. Conclusion
All seven test cases passed successfully. The `dns_analyzer.py` utility demonstrates robust input validation, flexible threshold tuning, and fault-tolerant exception handling, making it fully ready for inclusion in the Women Techsters Fellowship portfolio repository.
