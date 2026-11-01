# PowerShell Event Log Querying & Triage Guide

## 1. What PowerShell Is
PowerShell is an object-oriented task automation engine and command-line shell developed by Microsoft. Unlike traditional shells that output raw text, PowerShell processes inputs and outputs as structured .NET objects, making it ideal for event log analysis, script automation, and endpoint triage.

## 2. What `Get-WinEvent` Does
`Get-WinEvent` is a modern, high-performance PowerShell cmdlet used to query classic Windows event logs, ETW (Event Tracing for Windows) logs, and `.evtx` log files from local or remote computers.

## 3. How `-LogName` Works
The `-LogName` parameter specifies the target event log channel to query (e.g., `System`, `Application`, `Security`).
* **Actual Command Used:**
  ```powershell
  Get-WinEvent -LogName "System" -MaxEvents 10
``
4. How `-MaxEvents` Works
The `-MaxEvents` parameter caps the maximum number of matching event records returned by the query, preventing memory overload and speeding up execution time.
* **Actual Command Used:**
```powershell
Get-WinEvent -LogName "Security" -MaxEvents 50
```
### 5. What `-FilterHashtable` Does
`-FilterHashtable` passes structured key-value queries directly to the Windows Event Log database engine, filtering records before sending data to PowerShell. This provides fast query performance compared to slow text piping (`Where-Object`).

### 6. How to Filter by Time
Include the `StartTime` or `EndTime` key inside the filter hashtable:

* **Actual Command Used:**
```powershell
$StartTime = (Get-Date).AddHours(-24)
Get-WinEvent -FilterHashtable @{
    LogName   = 'System'
    StartTime = $StartTime
} -MaxEvents 50
```
### 7. How to Filter by Event ID
Include the `Id` key inside the filter hashtable, passing single IDs or arrays:

* **Actual Command Used:**
```powershell
Get-WinEvent -FilterHashtable @{
    LogName   = 'Security'
    Id        = @(4624, 4625, 4688)
    StartTime = (Get-Date).AddHours(-24)
} -MaxEvents 100
```
### 8. How `Select-Object` Works
`Select-Object` filters and extracts specified properties from incoming PowerShell objects.

* **Actual Command Used:**
```powershell
Get-WinEvent -LogName "System" -MaxEvents 5 | Select-Object TimeCreated, Id, ProviderName, Message
```
### 9. How `Export-Csv` Works
`Export-Csv` converts custom PowerShell objects into comma-separated text files. Using `-NoTypeInformation` keeps the output clean for analysis.

* **Actual Command Used:**
```powershell
$CollectedEvents | Export-Csv -Path ".\day-12\private-output\event-metadata.csv" -NoTypeInformation -Encoding UTF8
```
### 10. How to Handle Access Errors
Querying restricted logs (like Security) without sufficient permissions throws terminating errors. Wrap queries in `try/catch` blocks using `-ErrorAction Stop` to handle exceptions gracefully without crashing the script:

* **Actual Command Used:**
```powershell
try {
    Get-WinEvent -FilterHashtable @{ LogName = 'Security'; Id = 4624 } -MaxEvents 10 -ErrorAction Stop
} catch {
    Write-Warning "Access restricted or log unavailable: $($_.Exception.Message)"
}
