#!/usr/bin/env python3
"""
Project: SOC Interactive 9-Step Alert Triage Checklist & Report Generator
Author: Serah Mulwa
Day 14 - Cybersecurity Journey
Purpose: Guides Level 1 SOC analysts through a standardized 9-step alert triage
         workflow, ensuring full procedural compliance and compiling audit-ready 
         markdown handover reports.
"""

import sys
import os
from datetime import datetime

def print_header(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def prompt_step(step_num, step_name, instructions, default_val=None):
    print(f"\n[STEP {step_num}] — {step_name.upper()}")
    print(f"  Guidance: {instructions}")
    if default_val:
        try:
            user_input = input(f"  Enter details [Default: '{default_val}']: ").strip()
        except EOFError:
            user_input = ""
        return user_input if user_input else default_val
    else:
        while True:
            try:
                user_input = input("  Enter details: ").strip()
            except EOFError:
                user_input = "Sample Data"
            if user_input:
                return user_input
            print("  [!] Input cannot be empty. Please enter investigative details.")

def run_interactive_triage():
    print_header("SOC LEVEL 1 ALERT TRIAGE WORKFLOW CHECKLIST")
    print("Welcome Analyst. Follow the 9-step guided workflow to triage your alert.")

    # 0. Initial Metadata Gathering
    print_header("INITIAL ALERT METADATA")
    try:
        ticket_id = input("  • Alert / Ticket ID (e.g., ALT-2026-9901): ").strip() or "ALT-2026-9901"
    except EOFError:
        ticket_id = "ALT-2026-9901"

    try:
        rule_name = input("  • Triggering Rule Title: ").strip() or "SSH Brute Force Followed by Successful Authentication"
    except EOFError:
        rule_name = "SSH Brute Force Followed by Successful Authentication"

    try:
        target_host = input("  • Target Host (Hostname/IP): ").strip() or "PAYMENT-GATEWAY-01"
    except EOFError:
        target_host = "PAYMENT-GATEWAY-01"

    try:
        source_ip = input("  • Source IP Address: ").strip() or "185.220.101.5"
    except EOFError:
        source_ip = "185.220.101.5"

    # 1. Take Ownership
    ownership = prompt_step(
        1, "Take Ownership",
        "Confirm assignment, record start timestamp, and check for active duplicates in queue.",
        f"Claimed by Serah Kathini Mulwa at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}. No duplicates found."
    )

    # 2. Understand Detection
    detection_logic = prompt_step(
        2, "Understand Detection Logic",
        "Describe rule trigger conditions, thresholds, and detection limitations.",
        "Rule triggers on >= 10 failed SSH logins within 60s followed by successful auth on root account."
    )

    # 3. Identify Affected Entities
    entities = prompt_step(
        3, "Identify Affected Entities",
        "List all hosts, user accounts, processes, and network sockets involved.",
        f"Host: {target_host} | Account: root | Src IP: {source_ip} | Process: /usr/sbin/sshd"
    )

    # 4. Validate Evidence
    evidence = prompt_step(
        4, "Validate Underlying Evidence",
        "Verify raw event logs exist in SIEM/EDR, check timestamps, and ensure log integrity.",
        "Raw auth logs verified in /var/log/auth.log. 12 failed attempts followed by Event 4624 equivalent success."
    )

    # 5. Build Timeline
    timeline = prompt_step(
        5, "Build Chronological Timeline",
        "Provide chronological sequence of events (UTC).",
        "18:42:10 UTC - Failed auths; 18:42:38 UTC - Auth success; 18:43:02 UTC - 'cat /etc/passwd' executed."
    )

    # 6. Baseline Comparison
    baseline = prompt_step(
        6, "Compare Against Baseline",
        "Is this normal user/system behavior for this asset?",
        "Anomalous. Target account 'root' does not accept direct external SSH logins per security policy."
    )

    # 7. Check External Context
    context = prompt_step(
        7, "Check External Context",
        "Check Threat Intel (VirusTotal/AbuseIPDB), Change Requests, and asset inventory.",
        f"Source IP {source_ip} flagged as known Tor Exit Node on Threat Intel feeds. No approved change request."
    )

    # 8. Decide Disposition
    disposition = prompt_step(
        8, "Decide Disposition & Verdict",
        "Select Verdict: True Positive (TP), False Positive (FP), Benign Positive (BP), or Inconclusive.",
        "TRUE POSITIVE (TP) — Confirmed unauthorized access and post-compromise reconnaissance."
    )

    # 9. Document Reasoning & Actions
    actions = prompt_step(
        9, "Document Reasoning & Remediation Actions",
        "Detail investigative summary and required containment/escalation steps.",
        "Isolate PAYMENT-GATEWAY-01 immediately. Block 185.220.101.5 at edge firewall. Escalate to Tier 2 IR."
    )

    # Generate Markdown Incident Handover Report
    report_md = f"""# SOC INCIDENT TRIAGE & ESCALATION REPORT
**Ticket ID:** {ticket_id}  
**Date/Time:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}  
**Lead Analyst:** Serah Kathini Mulwa (Tier 1 SOC Analyst)  

---

### 1. ALERT METADATA & OWNERSHIP
* **Rule Title:** {rule_name}
* **Target Host:** `{target_host}`
* **Source IP:** `{source_ip}`
* **Ownership & Status:** {ownership}

---

### 2. DETECTION & ENTITY ANALYSIS
* **Detection Rule Logic:** {detection_logic}
* **Impacted Entities:** {entities}

---

### 3. FORENSIC EVIDENCE & CHRONOLOGICAL TIMELINE
* **Evidence Integrity:** {evidence}
* **Incident Timeline (UTC):**
  {timeline}

---

### 4. BASELINE & THREAT INTEL ENRICHMENT
* **Behavioral Baseline Analysis:** {baseline}
* **Threat Intel & Change Management Context:** {context}

---

### 5. FINAL DISPOSITION & ESCALATION HANDOVER
* **Final Classification Verdict:** **{disposition}**
* **Investigative Summary & Action Plan:**
  {actions}
"""

    print_header("TRIAGE WORKFLOW COMPLETE — GENERATING REPORT")
    print(report_md)

    # Save report to notes directory
    os.makedirs("day-14/notes", exist_ok=True)
    report_filename = "day-14/notes/triage-handover-report-sample.md"
    with open(report_filename, "w") as f:
        f.write(report_md)
    print(f"\n[+] Audit-ready handover report successfully written to: {report_filename}")

if __name__ == "__main__":
    run_interactive_triage()
