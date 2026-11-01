# PowerShell Event Log Triage & Investigation Notes - Day 12

## 1. PowerShell Environment Version (`$PSVersionTable`)
Executing `$PSVersionTable` in an administrator PowerShell session returned the following active environment specifications:
* **PSVersion:** `5.1.26100.9711`
* **PSEdition:** `Desktop`
* **OS / Build Version:** `10.0.26100.9711`
* **CLRVersion:** `4.0.30319.42000`

---

## 2. Event Log Channels Status & Record Counts (`Get-WinEvent -ListLog`)
Querying the metadata status of the primary Windows log channels via `Get-WinEvent -ListLog System,Application` verified that logging is active and populated:

| LogName | IsEnabled | RecordCount |
| :--- | :---: | :--- |
| **System** | True | 39,212 records |
| **Application** | True | 37,402 records |

---

## 3. Command Syntax & Query Output Summaries

### A. System Event Query (Top 10 Recent Events)
* **Command Syntax:**
  ```powershell
  Get-WinEvent -LogName System -MaxEvents 10 | Select-Object TimeCreated, Id, ProviderName, LevelDisplayName

  ```
 ### Execution Summary

Successfully retrieved the 10 most recent records from the System log channel. Key events observed included:

* **Event ID 6013** (`Source: EventLog`) — System uptime notification.
* **Event ID 158** (`Source: Microsoft-Windows-Time-Service`) — Time synchronization events.
* **Event ID 8265** (`Source: Microsoft-Windows-EnhancedPhishingProtection-Events`) — SmartScreen / Phishing protection telemetry.
* **Event ID 10016** (`Source: Microsoft-Windows-DistributedCOM`) — DCOM component permission warnings.

---

### B. Application Error Filter Query (`-FilterHashtable`)

#### Command Syntax:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName   = 'Application'
    Level     = 2
    StartTime = (Get-Date).AddDays(-7)
} -MaxEvents 20 | Select-Object TimeCreated, Id, ProviderName, LevelDisplayName

```
### Execution Summary
Leveraged high-performance hashtable filtering to isolate error-level (`Level = 2`) events in the Application log over the past 7 days. Results successfully filtered out routine info/warning telemetry, highlighting:

* **Event ID 1003** (`Source: CodexSandboxService.OpenAI.Codex`) — Application execution records.
* **Event ID 13** (`Source: Microsoft-Windows-AppModel-State`) — State repository deployment errors.

### 4. Key Analytical Takeaways & Memory Anchors

* **Object-Oriented Output:** PowerShell passes rich `.NET` objects (`Select-Object`) rather than static text streams. This allows analysts to extract specific properties (like `TimeCreated` or `Id`) instantly without complex regex parsing.
* **High-Performance Filtering (`-FilterHashtable`):** Utilizing `-FilterHashtable` passes query parameters directly to the underlying Windows event database engine rather than loading all records into memory first, drastically accelerating incident triage speed across massive enterprise event logs.
