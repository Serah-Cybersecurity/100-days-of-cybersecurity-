# Day 7 - Security Log Analyzer Test Results & Quality Assurance Report

| Test Case | Input Data | Expected Behaviour | Actual Observed Behaviour | Result |
| :--- | :--- | :--- | :--- | :--- |
| **1. Normal Dataset** | `sample_events.json` (5 valid records) | Five valid records loaded, correct event & failure counts. | Loaded 5 valid records, 0 invalid records, counted 3 failed logins successfully. | **Pass** |
| **2. Missing File** | Non-existent file path | Clean error message printed (`File not found`), no crash. | Displayed `Error: File not found` gracefully without crashing. | **Pass** |
| **3. Invalid JSON** | Malformed JSON syntax (missing comma) | JSON decode error reported cleanly. | Displayed `Error: The file does not contain valid JSON syntax.` | **Pass** |
| **4. Missing Field** | Incomplete record (missing `source_ip`) | Record rejected and flagged with missing field reason. | Flagged record with `Missing required fields: source_ip`. | **Pass** |
| **5. Wrong Top-Level Type** | JSON Object `{}` instead of List `[]` | Dataset rejected at top-level validation. | Displayed `Error: Expected a JSON list of event records.` | **Pass** |
| **6. Wrong Record Type** | Raw string inside list `["not an event object"]` | Individual record rejected as non-object. | Flagged record: `Record 0 is not a JSON object`. | **Pass** |
| **7. Empty List** | Empty JSON list `[]` | Processes without crashing, returning zero counts. | Processed successfully: 0 valid records, 0 invalid records, 0 failed logins. | **Pass** |

## Conclusion
All 7 defensive programming and exception handling test cases have been executed successfully via Windows PowerShell. The `security_log_analyzer.py` script demonstrates robust fault tolerance, graceful error handling, and strict schema validation under both normal and adversarial conditions.
