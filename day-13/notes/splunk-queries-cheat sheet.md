# Day 13 - Splunk Search Processing Language (SPL) Query Masterclass & Investigation Guide

* **Author:** Serah Mulwa  
* **Date:** October 31, 2026  
* **Environment:** Splunk Enterprise / Enterprise Security (SIEM)  
* **Target Audience:** Tier 1 SOC Analysts & Detection Engineers  

---

## 1. Executive Summary & SPL Mechanics

The **Splunk Search Processing Language (SPL)** is a unified query language used to search, filter, aggregate, transform, and visualize machine-generated telemetry. SPL operates as a sequential pipeline where data flows left-to-right through pipe characters (`|`). Each command modifies, filters, or structures the dataset passed to it by the preceding command.

```
┌────────────────────────────────┐
│ 1. Base Filter (Disk Index)    │  index=security EventCode=4625
└───────────────┬────────────────┘
                │ |
                ▼
┌────────────────────────────────┐
│ 2. Aggregation & Transformation│  stats count BY IpAddress, TargetUserName
└───────────────┬────────────────┘
                │ |
                ▼
┌────────────────────────────────┐
│ 3. Boolean Evaluation          │  where count > 5
└───────────────┬────────────────┘
                │ |
                ▼
┌────────────────────────────────┐
│ 4. Sorting & Output Limit      │  sort - count | head 10
└────────────────────────────────┘
```

---

## 2. Core Command Reference Table

| Command | Category | Function & Usage | Example Syntax |
| :--- | :--- | :--- | :--- |
| **`index=`** | Base Search | Restricts search to a specific logical database index. | `index=security` |
| **`sourcetype=`** | Base Search | Filters by log format driver/parser. | `sourcetype=WinEventLog:Security` |
| **`fields`** | Optimization | Keeps or removes specified fields from memory pipeline. | `\| fields _time, host, user, src_ip` |
| **`table`** | Output Formatting | Renders selected fields into clean tabular columns. | `\| table _time, host, TargetUserName, IpAddress` |
| **`rename`** | Formatting | Re-labels field names for reporting clarity. | `\| rename TargetUserName AS User, IpAddress AS Source_IP` |
| **`stats`** | Aggregation | Calculates statistical metrics (`count`, `dc`, `values`, `avg`, `sum`). | `\| stats count dc(TargetUserName) BY IpAddress` |
| **`eval`** | Field Transformation| Evaluates mathematical/string operations to create dynamic fields. | `\| eval Risk_Level=if(count>10, "HIGH", "LOW")` |
| **`where`** | Filtering | Filters aggregated metrics using boolean expressions. | `\| where count >= 5` |
| **`sort`** | Ordering | Sorts results ascending (`+`) or descending (`-`). | `\| sort - count` |
| **`dedup`** | Deduplication | Removes duplicate events based on field matching. | `\| dedup TargetUserName` |
| **`head` / `tail`** | Output Limit | Limits results to the top $N$ or bottom $N$ rows. | `\| head 10` |

---

## 3. Standard SOC Investigation Queries

### Query 1: Windows Brute-Force & Credential Stuffing Detection
* **Objective:** Identify top external IP addresses attempting multiple failed logins across local user accounts.
* **Target Schema:** Windows Security Event Log (`EventCode 4625`).
* **Time Range:** `earliest=-24h@h latest=now`

```spl
index=security sourcetype=WinEventLog:Security EventCode=4625
| stats count AS failed_attempts, dc(TargetUserName) AS unique_targets, values(TargetUserName) AS targeted_accounts BY IpAddress
| where failed_attempts >= 5
| sort - failed_attempts
| rename IpAddress AS Attacker_IP
```

### Query 2: Remote Desktop Protocol (RDP) Successful Authentication Tracking
* **Objective:** Detect successful RDP interactive logins (`LogonType 10`) originating from non-standard subnets.
* **Target Schema:** Windows Security Event Log (`EventCode 4624`).

```spl
index=security sourcetype=WinEventLog:Security EventCode=4624 LogonType=10
| eval Network_Location = if(cidrmatch("10.0.0.0/8", IpAddress), "Internal", "External_WAN")
| table _time, host, TargetUserName, IpAddress, Network_Location, WorkstationName
| sort - _time
```

### Query 3: Suspicious Process Execution Lineage (Command-Line Auditing)
* **Objective:** Detect execution of command interpreters (`cmd.exe` or `powershell.exe`) spawning encoded script blocks or web download requests.
* **Target Schema:** Windows Process Creation (`EventCode 4688` / Sysmon `EventID 1`).

```spl
index=security (EventCode=4688 OR EventCode=1) (NewProcessName="*\\powershell.exe" OR NewProcessName="*\\cmd.exe")
| search CommandLine="*DownloadString*" OR CommandLine="*Invoke-WebRequest*" OR CommandLine="*-enc*"
| table _time, host, SubjectUserName, ParentProcessName, NewProcessName, CommandLine
| sort - _time
```

### Query 4: Linux SSH Authentication Failure Analysis
* **Objective:** Aggregate failed SSH authentication attempts by source IP and target user accounts on Linux infrastructure.
* **Target Schema:** Linux Secure / Auth log (`sourcetype=linux_secure` or `syslog`).

```spl
index=linux sourcetype=linux_secure "Failed password"
| stats count BY src_ip, user, host
| sort - count
| head 15
```

### Query 5: Security Event Log Clearing Audit (Anti-Forensics Indicator)
* **Objective:** Alert immediately on any attempt to clear the Windows Security Event Log (`EventCode 1102`).
* **Target Schema:** Windows Security Log.

```spl
index=security sourcetype=WinEventLog:Security EventCode=1102
| table _time, host, SubjectUserName, SubjectUserSid, Message
```

---

## 4. Query Documentation & Investigation Logs

When conducting SOC triage or incident response, document your SPL execution parameters using the following standardized template:

```markdown
### Investigation Log #20261031-01
* **Incident Title:** Potential Brute-Force Authentication Sequence
* **Analyst Name:** Serah Mulwa
* **Date / UTC Time:** 2026-10-31T14:30:00Z
* **Target Index / Sourcetype:** `index=security sourcetype=WinEventLog:Security`
* **Time Range Selector:** `earliest=2026-10-31T00:00:00Z latest=2026-10-31T14:00:00Z`
* **Executed Query:**
  ```spl
  index=security EventCode=4625 
  | stats count BY IpAddress, TargetUserName 
  | sort - count 
  | head 10
  ```
* **Aggregated Output Findings:**
  * Total Events Analyzed: `1,428`
  * Top Offending IP: `192.168.1.105`
  * Target Username: `admin`
  * Total Failed Attempts: `1,420` within a 15-minute execution window ($\Delta t = 900\text{s}$).
* **Analytical Conclusion:** High-confidence automated credential stuffing attack. Host containment ticket opened.
```

---

## 5. Core SPL Rules for Analysts

> 💡 **Rule 1: Filter Early in the Pipeline.** Always specify `index=`, `sourcetype=`, and explicit time limits (`earliest=`/`latest=`) before applying pipe (`|`) transformations to avoid memory bottlenecks.

> 💡 **Rule 2: Never Trust Raw Field Names.** Vendor field names vary. Use `rename` or normalized Common Information Model (CIM) terms (`user`, `src_ip`, `action`) when compiling final report tables.

> 💡 **Rule 3: Deduplicate Before Counting Unique Entities.** Use `dc(field)` (distinct count) rather than `count` when measuring compromised accounts or accessed systems.
