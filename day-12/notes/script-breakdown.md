# Script Architecture & Code Breakdown Notes - Day 12

## 1. Parameter Validation (`[ValidateRange]`)
* **What it is:** Parameter validation attributes (such as `[ValidateRange(1, 168)]`) are built-in PowerShell safety filters placed inside the `param()` block.
* **Why it matters:** They enforce strict numerical boundaries on dynamic user inputs before script execution begins. For example, restricting `$HoursBack` between 1 and 168 hours (7 days) prevents an operator or automated utility from accidentally passing an unbounded value (e.g., `-HoursBack 5000`), which would attempt to query years of historical logs, exhaust local endpoint memory, and freeze the operating system.
* **Job Market Application:** In enterprise security engineering, robust input validation is a foundational defensive coding practice that prevents resource exhaustion attacks and operational errors during incident response.

---

## 2. Multi-Log Queries Using Hashtables
* **What it is:** Hashtables (`@{ Key = Value }`) store key-value data pairs. In `Get-Day12EventSummary.ps1`, an array of hashtables (`$Queries`) defines the log channels and target Event IDs to investigate.
* **Why it matters:** Hashtable structures provide clean modularity. Instead of hardcoding separate query blocks for every individual log, the script loops through a dynamic configuration list. This allows security analysts to add new log channels (such as `Setup` or custom application logs) instantly by appending a new hashtable block without rewriting the core scanning engine.
* **Performance Benefit:** Passing these hashtables directly into the `-FilterHashtable` parameter of `Get-WinEvent` enables high-performance, database-level filtering directly within the underlying Windows event log engine.

---

## 3. Error Resilience via `try/catch` Exception Handling
* **What it is:** The script wraps core query operations in `try/catch` logic combined with `-ErrorAction Stop`, intercepting operational failures (such as permission denials on restricted channels like Security).
* **Why it matters:** During live endpoint triage, encountering an access-restricted log channel or missing data should never cause a script to crash catastrophically halfway through execution. Robust error resilience catches the exception, logs a descriptive warning message, and gracefully allows the script to continue scanning remaining log channels (such as System and Application).
* **Job Market Application:** Production-grade security scripts must be fault-tolerant. Enterprise triage tools fail audit reviews if they crash upon hitting permission walls.

---

## 4. The Privacy Rationale Behind Metadata-Only Collection
* **What it is:** The script intentionally extracts and packages only essential structural metadata (`TimeCreated`, `EventId`, `Provider`, `Level`, `RecordId`) into custom PowerShell objects (`[PSCustomObject]`), while explicitly **omitting full raw event message bodies**.
* **Why it matters:** Full Windows event message strings frequently contain sensitive personal data, internal local workstation names, private domain paths, and client IP addresses. Exporting unredacted message text into output files creates a severe compliance and security risk when pushing code repositories to public version control platforms like GitHub.
* **Security Principle:** Collecting structured metadata provides 100% of the statistical inventory required for initial threat scoping and reporting while strictly maintaining data privacy hygiene.
