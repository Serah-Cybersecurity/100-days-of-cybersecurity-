# Day 13 - Log Normalization & Common Schema Architecture

* **Author:** Serah Mulwa  
* **Date:** October 31, 2026  
* **Module:** SIEM Fundamentals & Log Engineering  
* **Target Audience:** Tier 1 SOC Analysts & Detection Engineers  

---

## 1. The Multi-Source Log Disconnect (The Problem)

In any enterprise environment, security telemetry arrives from dozens of different vendors, operating systems, and network appliances. Each vendor speaks its own "dialect":

* **Windows Active Directory (Security Log):** Uses numeric Event IDs like `4625` (failed login) or `4624` (successful login), with field names such as `TargetUserName` and `IpAddress`.
* **Linux Operating System (`/var/log/auth.log` / `sshd`):** Uses text labels like `Failed password for ...` or `Accepted publickey`, exposing fields like `user` and `src_ip`.
* **Perimeter Firewalls (Palo Alto / Cisco ASA):** Uses traffic codes like `FW_DENY` or `FW_ALLOW`, with field labels such as `src` and `dst`.

Without **log normalization**, writing a detection rule for a brute-force attack would require four completely different scripts or query syntaxes for Windows, Linux, firewalls, and cloud applications.

---

## 2. What is Log Normalization?

**Log normalization** is the process of translating disparate vendor-specific log formats into a standardized, unified schema (such as Splunk's Common Information Model or Elastic Common Schema). 

By mapping unique vendor terms into shared parameters, analysts can query multi-platform datasets using a single universal syntax.

### Our Simplified Common Schema
In our Mini-SIEM project, we standardize events into nine common fields:
1. `timestamp`: ISO 8601 normalized event time.
2. `host`: Originating endpoint hostname.
3. `platform`: Operating system or infrastructure tier (`windows`, `linux`, `network`).
4. `source`: Specific log subsystem (`Security`, `sshd`, `firewall`).
5. `event_id`: Vendor-specific code or label (`4625`, `SSH_FAIL`, `FW_DENY`).
6. `event_type`: High-level category (`authentication`, `network`, `process`, `service`).
7. `username`: Standardized user identity.
8. `src_ip`: Standardized source IP address.
9. `result`: Standardized action outcome (`success`, `failure`, `denied`, `allowed`).

---

## 3. Deep-Dive: Core Normalization Principles

### 3.1 What a `source` Field Means
* **Definition:** Identifies the specific subsystem, daemon, or log provider on the host that generated the event.
* **Example:** `Security` (Windows EVTX), `sshd` (Linux OpenSSH daemon), or `firewall` (Perimeter packet filter).
* **Why it matters:** Allows investigators to isolate events down to the exact software component responsible for logging the activity.

### 3.2 What a `platform` Field Means
* **Definition:** Broadly categorizes the operating environment or infrastructure layer of the asset.
* **Example:** `windows`, `linux`, `network`, or `cloud`.
* **Why it matters:** Enables high-level executive dashboards and macro-level filtering (e.g., viewing all alerts originating strictly from Linux infrastructure).

### 3.3 What an `event_type` Represents
* **Definition:** A high-level behavioral category that transcends specific vendor event codes.
* **Example:** Grouping Windows Event ID `4625`, Linux `SSH_FAIL`, and Firewall `FW_DENY` under a single universal `event_type: authentication` or `network`.
* **Why it matters:** Allows security analysts to write correlation rules that catch attacks regardless of whether they happen on a Windows laptop or a Linux cloud server.

### 3.4 Why Usernames Should Use Consistent Field Names
* **The Issue:** Windows logs use `TargetUserName`, Linux logs use `user`, and AWS CloudTrail uses `userIdentity.userName`.
* **The Solution:** Normalizing all user references into a single field name: `username`.
* **Why it matters:** Ensures that aggregation commands (`stats count by username`) work universally across all platforms without writing complex `coalesce()` conditional logic.

### 3.5 Why Timestamps Must Include Time-Zone Information
* **The Issue:** Local server clocks, UTC logs, and regional time zones create conflicting event sequences during investigations.
* **The Solution:** Enforcing ISO 8601 timestamps with explicit UTC offsets (e.g., `2026-10-31T08:00:00+03:00`).
* **Why it matters:** Precise chronological ordering is critical when calculating temporal deltas ($\Delta t$) during multi-source attack reconstruction.

### 3.6 Why Unavailable Fields Should Be Represented Consistently
* **The Issue:** Network packet logs do not have a `username`, and some host process events do not involve a `src_ip`. Leaving fields out entirely causes parsing errors in scripts.
* **The Solution:** Representing missing or inapplicable fields consistently as `null` (JSON) or `None` (Python).
* **Why it matters:** Keeps data schemas uniform and prevents runtime null-pointer exceptions in automated analysis scripts.

### 3.7 Why Original Source Information Must Still Be Preserved
> ⚠️ **Critical Rule:** *Normalization must never destroy raw context.*
* **The What:** While you map fields into a common schema, you must always retain the original raw log string (`_raw` in Splunk or the original JSON object).
* **Why it matters:** In court, compliance audits, or complex incident investigations, analysts must be able to verify that the normalized interpretation matches the original forensic artifact without data distortion.

---

## 4. How Normalization is Applied in the Job Market

* **SOC Tier 1 & Threat Hunting:** Analysts rely on normalized fields to write universal correlation rules (like Sigma or Splunk Enterprise Security notable events) that trigger regardless of whether an endpoint runs Windows 11 or Red Hat Enterprise Linux.
* **Compliance Audits:** Auditors require proof that multi-vendor logs are ingested, indexed, and normalized to ensure reliable log retention and integrity verification.

---

## 5. Core Analyst Axioms

> 💡 **Axiom 1:** *Normalization is the bridge between chaotic vendor logs and automated threat detection.*  
> 💡 **Axiom 2:** *Never discard raw event context when standardizing fields; always preserve the source of truth.*
