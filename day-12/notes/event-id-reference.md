# Windows Security Event ID Reference Guide - Day 12

## Overview
This reference guide details the six core Windows Security Event IDs utilized by Security Operations Centre (SOC) analysts, threat hunters, and incident response practitioners to detect authentication anomalies, privilege escalation, process execution, and audit log tampering.

---

## 1. Core Event IDs Detailed Analysis

### 1. Event ID 4624 - Successful Logon
* **Channel:** Security
* **Description:** Generated on the target system when an account successfully authenticates and creates a logon session.
* **Key Diagnostic Fields:**
  * `TargetUserName`: The account that authenticated.
  * `TargetDomainName`: Domain or local machine evaluating credentials.
  * `LogonType`: Numeric identifier representing the logon mechanism.
  * `TargetLogonId`: Hexadecimal session identifier (used to correlate with Event ID 4672 and 4634).
  * `IpAddress` / `WorkstationName`: Originating network source details.
* **Logon Type Quick Reference:**
  * **Type 2 (Interactive):** Direct physical sign-in at the local keyboard/console.
  * **Type 3 (Network):** Accessing shared folders, network drives, IIS, or WinRM.
  * **Type 4 (Batch):** Scheduled tasks running under user context.
  * **Type 5 (Service):** Background Windows services starting up.
  * **Type 7 (Unlock):** Unlocking a locked screen.
  * **Type 10 (RemoteInteractive):** Remote Desktop Protocol (RDP) session.
  * **Type 11 (CachedInteractive):** Local sign-in using cached domain credentials offline.
* **SOC Analyst Context:** A successful logon is not inherently benign. Analysts must verify whether Logon Type 10 (RDP) or Type 3 (Network) originates from approved corporate IP addresses.

---

### 2. Event ID 4625 - Failed Logon
* **Channel:** Security
* **Description:** Recorded on the target system when an authentication attempt is rejected.
* **Key Diagnostic Fields:**
  * `TargetUserName`: Account attempted.
  * `IpAddress`: Source IP address initiating the failure.
  * `FailureReason` / `Status` / `SubStatus`: Hexadecimal error codes detailing failure causes:
    * `0xC000006A`: Incorrect password.
    * `0xC0000064`: Non-existent user account.
    * `0xC0000234`: User account locked out.
* **SOC Analyst Context:** Spikes in 4625 records indicate brute-force attempts or automated password spraying. A high volume of 4625 failures followed immediately by a single 4624 success from the same source IP signifies a potential credential compromise.

---

### 3. Event ID 4672 - Special Privileges Assigned
* **Channel:** Security
* **Description:** Recorded when administrative or elevated system privileges are assigned to a newly created logon session.
* **Key Diagnostic Fields:**
  * `SubjectUserName`: Account assigned privileges.
  * `TargetLogonId`: Matches the `TargetLogonId` from the corresponding 4624 event.
  * `PrivilegeList`: Rights granted (e.g., `SeDebugPrivilege`, `SeTakeOwnershipPrivilege`, `SeImpersonatePrivilege`).
* **SOC Analyst Context:** Generated routinely during administrative logons and system service starts (`SYSTEM`, `LOCAL SERVICE`). It warrants investigation if assigned to non-administrative user accounts or standard workstations.

---

### 4. Event ID 4688 - A New Process Was Created
* **Channel:** Security
* **Description:** Recorded when a new program or process is spawned on the host system.
* **Key Diagnostic Fields:**
  * `NewProcessName`: Full file path of the executed program (e.g., `C:\Windows\System32\cmd.exe`).
  * `ParentProcessName`: Executable that spawned the new process (e.g., `explorer.exe` or `WINWORD.EXE`).
  * `CommandLine`: Complete command string executed (requires enabling *Include command line in process creation events* in Group Policy).
* **SOC Analyst Context:** Primary telemetry source for detecting post-exploitation activity, script execution (PowerShell/CMD), living-off-the-land binaries (Lolbins), and malicious email macro executions (e.g., Word spawning PowerShell).

---

### 5. Event ID 1102 - Security Audit Log Cleared
* **Channel:** Security
* **Description:** Explicitly logged when the Windows Security Event Log file is manually cleared.
* **Key Diagnostic Fields:**
  * `SubjectUserName`: Account that executed the log clear action.
  * `SubjectLogonId`: Session ID associated with the user clearing logs.
* **SOC Analyst Context:** High-severity defense evasion alert. Adversaries frequently attempt to erase evidence (`wevtutil cl Security`). Any occurrence must be validated against authorized administrative maintenance schedules.

---

### 6. Event ID 4634 - Account Logoff
* **Channel:** Security
* **Description:** Logged when a user session is closed and the account logs off.
* **Key Diagnostic Fields:**
  * `TargetUserName`: Account logging off.
  * `TargetLogonId`: Matches the session ID from Event ID 4624.
  * `LogonType`: Mechanism used during the session.
* **SOC Analyst Context:** Used in forensic timeline construction. Subtracting the Event 4624 timestamp from the Event 4634 timestamp reveals the exact active duration of an adversary or user session.

---

## 2. Summary Quick-Reference Table

| Event ID | Log Channel | Category | Primary Telemetry | High-Value SOC Use Case |
| :---: | :---: | :--- | :--- | :--- |
| **4624** | Security | Successful Logon | Target Account, Logon Type, Source IP, Logon ID | Verify remote logons (Type 10 RDP, Type 3 Network) & lateral movement. |
| **4625** | Security | Failed Logon | Target Account, Source IP, Failure SubStatus | Detect brute-force attacks and password spraying attempts. |
| **4672** | Security | Special Privileges | Account Name, Logon ID, Privilege List | Identify privilege escalation; link to 4624 session via Logon ID. |
| **4688** | Security | Process Creation | Executable Path, Parent Process, Command Line | Track command execution, malicious scripts, and parent-child process anomalies. |
| **1102** | Security | Audit Log Cleared | User Account, Logon ID | Defense evasion detection; trigger immediate high-priority triage. |
| **4634** | Security | Account Logoff | Target Account, Logon ID, Logon Type | Calculate precise adversary session duration on host. |
