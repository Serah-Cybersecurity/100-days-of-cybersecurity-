# Important Security & System Event IDs Reference

## 1. Event ID 4624 - Successful User Authentication
* **Event Description:** An account was successfully logged on to the local computer or network resource.
* **Recorded Log:** `Security`
* **Why it Matters:** Verifies successful access to an endpoint. It allows analysts to track logon frequency, identify remote desktop access, monitor service logons, and validate user session initiation.
* **Fields Worth Examining:**
  * `TargetUserName`: The user account that authenticated.
  * `LogonType`: Identifies how the user logged in (e.g., Type 2 = Interactive keyboard logon, Type 3 = Network share access, Type 5 = Service account logon, Type 10 = Remote Desktop / RDP).
  * `TargetLogonId`: Unique hex session identifier (`0x3E7`) used to correlate subsequent user actions.
  * `IpAddress`: Source IP address initiating the connection.
* **Common Misinterpretation:** Assuming every 4624 event indicates human activity. In reality, system background processes and service accounts continuously generate Type 5 service logons automatically.
* **Official Reference:** [Microsoft Security Audit 4624](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4624)

---

## 2. Event ID 4625 — Failed User Authentication
* **Event Description:** An account failed to log on to the system.
* **Recorded Log:** `Security`
* **Why it Matters:** High-priority indicator for brute-force attacks, password-spraying attempts, or misconfigured application service accounts.
* **Fields Worth Examining:**
  * `TargetUserName`: The account name targeted by the failed login attempt.
  * `Status` / `SubStatus`: Hexadecimal error codes detailing why the login failed (e.g., bad password `0xC000006A`, account locked out `0xC0000234`, user non-existent `0xC0000064`).
  * `WorkstationName` & `IpAddress`: Source location initiating the unauthorized authentication attempt.
* **Common Misinterpretation:** Jumping to the conclusion that a single failed 4625 means an active cyberattack. Users frequently mistype passwords or fail to update cached credentials in mapped drives.
* **Official Reference:** [Microsoft Security Audit 4625](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4625)

---

## 3. Event ID 4672 — Special Privileges Assigned to New Logon
* **Event Description:** Administrative rights or sensitive user rights were assigned to a newly established user logon session.
* **Recorded Log:** `Security`
* **Why it Matters:** Identifies when a logon session gains administrative capabilities (e.g., `SeDebugPrivilege`, `SeTakeOwnershipPrivilege`, `SeBackupPrivilege`), highlighting high-privilege sessions.
* **Fields Worth Examining:**
  * `SubjectUserName`: Account receiving elevated rights.
  * `SubjectLogonId`: Must match the `TargetLogonId` from the corresponding 4624 event.
  * `Privileges`: List of assigned administrative privileges.
* **Common Misinterpretation:** Assuming 4672 always means a user escalated privileges maliciously. Standard local administrator logins automatically generate 4672 upon logging in.
* **Official Reference:** [Microsoft Security Audit 4672](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4672)

---

## 4. Event ID 4688 — Process Creation
* **Event Description:** A new process has been launched on the host operating system.
* **Recorded Log:** `Security`
* **Why it Matters:** Fundamental to process execution tracking, detecting malicious command-line execution (`cmd.exe`, `powershell.exe`, `certutil.exe`), and analyzing malware process trees.
* **Fields Worth Examining:**
  * `NewProcessName`: Full file-system path of the executable being launched.
  * `CommandLine`: The exact arguments passed during execution (requires Group Policy enablement).
  * `ParentProcessName`: Executable path of the parent process that spawned the new process.
  * `SubjectLogonId`: Session context under which the process was executed.
* **Common Misinterpretation:** Assuming process creation alone proves malicious activity. Windows launches dozens of legitimate system background processes continuously.
* **Official Reference:** [Microsoft Security Audit 4688](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4688)

---

## 5. Event ID 1102 — Security Audit Log Cleared
* **Event Description:** The Windows Security Event Log was intentionally cleared by a user or script.
* **Recorded Log:** `Security`
* **Why it Matters:** Major anti-forensics flag. Attackers clear logs to erase evidence of intrusion, privilege escalation, and lateral movement.
* **Fields Worth Examining:**
  * `SubjectUserName`: Account that executed the clearing action.
  * `SubjectDomainName` & `SubjectLogonId`: Identity and session correlation context.
* **Common Misinterpretation:** Assuming log clearing is always malicious. System administrators sometimes clear logs during routine maintenance or after completing local software testing.
* **Official Reference:** [Microsoft Security Audit 1102](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-1102)

---

## 6. Event ID 7045 — Service Installation
* **Event Description:** A new background system service was installed on the machine.
* **Recorded Log:** `System`
* **Why it Matters:** Key persistence and privilege escalation indicator. Adversaries frequently install custom Windows services or modify service binaries to retain SYSTEM access across reboots.
* **Fields Worth Examining:**
  * `ServiceName`: Name of the newly registered service.
  * `ImagePath`: File path and command arguments assigned to the service executable.
  * `ServiceType` & `StartType`: Details whether the service runs as SYSTEM and if it boots automatically.
* **Common Misinterpretation:** Flagging every 7045 as a backdoor. Software installations, anti-virus updates, and Windows updates routinely install legitimate services.
* **Official Reference:** [Microsoft System Event 7045 Reference](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-7045)
