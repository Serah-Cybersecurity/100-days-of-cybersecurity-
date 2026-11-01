# Deep Dive: Core Analyst Axioms & Concepts

When a SOC Lead or Senior Forensic Investigator reviews an incident report, they look for defensibility, precision, and technical structure. Here is how to execute your documentation and mindset to enterprise standards:

```
                  ┌─────────────────────────────────────────┐
                  │       DEFENSIBLE INVESTIGATION          │
                  └────────────────────┬────────────────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         ▼                             ▼                             ▼
┌─────────────────┐           ┌─────────────────┐           ┌─────────────────┐
│ 1. SOURCE       │           │ 2. TEMPORAL     │           │ 3. CORRELATION  │
│    IDENTIFIERS  │           │    ALIGNMENT    │           │    RULE MATCH   │
│ (Endpoints/IPs) │           │ (Normalized UTC)│           │ (SIEM Signature)│
└─────────────────┘           └─────────────────┘           └─────────────────┘
```

---

## 1. What to Document in an Investigation Note (Deep Breakdown)

### A. Source Identifiers (Host, Network & Identity Mapping)
You must record every unique asset identifier involved across the operational path. Never rely on just a username or just an IP address.

* **Target Hostnames:** Record both the NetBIOS local computer name (`HR_02`, `MY-BABY`) and Fully Qualified Domain Name (FQDN) (e.g., `HR_02.corp.internal`).
* **IP Addresses (Source vs. Destination):**
  * **Source IP (Attacker or Initiator):** `192.168.1.105` (Internal LAN) or `203.0.113.50` (External WAN).
  * **Destination IP (Target Asset):** `10.0.0.12` (Database Server).
* **Identity Context (User & Account SID):**
  * **Target User Account:** `admin`, `finance_mgr`, `s_mulwa`.
  * **Security Identifier (SID):** `S-1-5-21-...-500` (Crucial for tracking renamed or impersonated accounts).
* **Process & Application Metadata:** Executable binary paths (`C:\Windows\System32\cmd.exe`), process IDs (`PID 4128`), and application services.

### B. Temporal Alignment (Normalized UTC Timestamps)
Time variance is the fastest way to ruin a forensic investigation. If System A is set to EST (UTC-5) and System B is set to EAT (UTC+3), looking at raw timestamps makes an event at 09:00 AM on System B look like it happened hours before an event at 09:00 AM on System A.

* **Always Normalize to UTC (`Z` / `+00:00`):** Express every timestamp in International ISO 8601 format: `2026-10-31T14:00:15Z`.
* **Calculate Relative Deltas ($\Delta t$):** Record the exact elapsed time between sequence steps.
  * *Example:* "Failed login attempt #3 occurred at 14:00:09Z. Successful logon occurred at 14:00:15Z ($\Delta t = 6 \text{ seconds}$). This tight timeframe rules out human password entry and confirms script automation."
* **Log Ingestion Delay (Latency):** Note if there is a gap between when the event occurred on the host (`_time`) and when the SIEM ingested it (`_indextime`).

### C. Correlation Rule Match (Alert Trigger & Signature Context)
Document the exact mechanical rules that raised the alarm.

* **SIEM Signature Name:** `CORRELATED_BRUTE_FORCE_SUCCESS` or `Win_Event_4625_Threshold_Exceeded`.
* **Rule Threshold Logic:** Document the mathematical trigger condition:
  $$\text{Failed Logins} \ge 3 \quad \text{AND} \quad \text{Successful Logon} = 1 \quad \text{within } \Delta t \le 300\text{s}$$
* **SIEM Query String Used:** Copy the exact SPL or KQL query used to aggregate the logs (e.g., `index=security EventCode=4625 | stats count BY IpAddress | where count >= 3`).
* **MITRE ATT&CK Mapping:** Map the alert to standard threat frameworks:
  * **Tactic:** Credential Access (`TA0006`)
  * **Technique:** Brute Force (`T1110.001`)

---

## 2. What I Must Remember (The Core Analyst Axioms)

> 💡 **Axiom 1: Isolated Logs Hide Attacks; Centralized Correlation Exposes Them.**  
> A single failed login is system noise. A failed login followed by a successful logon, an SSH connection to a database, and an outbound connection denied by a firewall is a critical breach in progress.

> 💡 **Axiom 2: Authentication Mechanics $\neq$ Human Intent.**  
> Event ID 4624 proves that valid credentials were accepted by the operating system. It does not prove that the authorized employee entered them. Always evaluate the source IP, Logon Type, and preceding failed authentication records (4625).

> 💡 **Axiom 3: Never Alter Original Telemetry.**  
> Investigation notes, scripts, and SIEM queries must be strictly read-only. You collect and correlate facts—you never alter source event channels or erase host logs.

> 💡 **Axiom 4: Telemetry Gaps Must Be Documented, Not Ignored.**  
> If an endpoint lacks firewall logs or process command-line auditing, document it as an operational limitation. *Absence of evidence is not evidence of absence.*
