# DAY 14: TEST RESULTS & VALIDATION REPORT

**Date:** November 2, 2026  
**Analyst:** Serah Kathini Mulwa (Tier 1 SOC Analyst)  
**Target Script:** `day-14/scripts/triage_queue.py`  
**Dataset:** `day-14/lab/data/alert-queue.jsonl`  
**Test Status:** PASSED (100% Success Rate)

---

## 1. EXECUTIVE TEST SUMMARY

This report documents the verification and test execution results for the custom Python utility script `triage_queue.py`. The objective was to validate that the script correctly ingests, verifies schemas, normalizes timestamps to UTC, sorts by operational severity, and tallies alert counts without assigning automated malicious/benign verdicts.

---

## 2. VERIFICATION METRICS

| Metric | Expected Value | Actual Value | Status |
| :--- | :--- | :--- | :--- |
| **Total Lines Processed** | 3 | 3 | PASSED |
| **Valid Alerts Loaded** | 3 | 3 | PASSED |
| **Invalid / Malformed Records** | 0 | 0 | PASSED |
| **Schema Validation Errors** | 0 | 0 | PASSED |
| **Execution Exit Code** | 0 | 0 | PASSED |

---

## 3. PROCESSED ALERT QUEUE BREAKDOWN

### Case Breakdown (Sorted by Priority & UTC Time)

1. **Alert ID:** `SOC-2026-001`
   * **Title:** Repeated Failed Logons Followed by Successful Logon
   * **Severity:** `HIGH`
   * **Status:** `new`
   * **Target Host:** `WIN-LAB-01`
   * **Rule ID:** `AUTH-003`
   * **Timestamp:** `2026-11-01T08:04:15+03:00` $\rightarrow$ Converted to `05:04:15 UTC`
   * **Summary:** Three failed authentication events followed by a successful logon.

2. **Alert ID:** `SOC-2026-002`
   * **Title:** Failed SSH Authentication
   * **Severity:** `MEDIUM`
   * **Status:** `new`
   * **Target Host:** `LINUX-LAB-01`
   * **Rule ID:** `SSH-FAIL-001`
   * **Timestamp:** `2026-11-01T08:21:30+03:00` $\rightarrow$ Converted to `05:21:30 UTC`
   * **Summary:** One failed SSH authentication followed by a successful login.

3. **Alert ID:** `SOC-2026-003`
   * **Title:** New Service Started
   * **Severity:** `MEDIUM`
   * **Status:** `new`
   * **Target Host:** `WIN-LAB-01`
   * **Rule ID:** `SERVICE-START-001`
   * **Timestamp:** `2026-11-01T08:30:10+03:00` $\rightarrow$ Converted to `05:30:10 UTC`
   * **Summary:** The backup-agent service started as expected.

---

## 4. SEVERITY SUMMARY OUTPUT

```text
===== SEVERITY SUMMARY =====
high: 1
medium: 2
```

---

## 5. DEFENSIVE PROGRAMMING & ERROR HANDLING VALIDATION

The script was also evaluated against edge cases and malformed schemas:

* **Missing Key Handling:** Verified that any JSON line missing required keys (`created_at`, `host`, `rule_id`, `status`, `summary`, `title`, `severity`, `alert_id`) is safely caught, reported to `sys.stderr` with exact line numbers, and skipped without halting script execution.
* **Timestamp Normalization:** Verified that ISO-8601 strings containing timezone offsets are correctly parsed and converted to timezone-aware UTC objects.
* **Separation of Concerns:** Confirmed that the script does not auto-assign verdicts, preserving the analyst's operational duty to perform context checks against `case-context.md`.

---

## 6. CONCLUSION & RECOMMENDATIONS

The script `triage_queue.py` has passed all testing criteria and is approved for production integration into the Day 14 SOC workflow suite.
