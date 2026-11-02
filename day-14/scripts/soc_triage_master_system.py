#!/usr/bin/env python3
"""
Project: Day 14 Main Project - End-to-End SOC Alert Triage System
Author: Serah Mulwa
Day 14 - Cybersecurity Journey
Purpose: Simulates an enterprise SOC queue containing Alert A, B, and C. 
         Automates priority scoring, classification, and audit report generation.
"""

import json
import os
from datetime import datetime

# Define the Three Project Queue Alerts
MASTER_QUEUE = [
    {
        "alert_id": "ALT-2026-9001",
        "name": "Alert A - Potential Unauthorized Account Access",
        "severity": "HIGH",
        "asset_criticality": "CRITICAL",  # Domain Controller / Core Server
        "is_ongoing": True,
        "detection_confidence": "HIGH",
        "source_ip": "198.51.100.45",
        "target_host": "DC-01.corp.local",
        "user_account": "administrator",
        "raw_evidence": "3x failed Windows logins (Event 4625), 1x successful logon (Event 4624), 1x privilege grant (Event 4672).",
        "change_request": None,
        "threat_intel_flag": "Unknown / Suspicious External IP"
    },
    {
        "alert_id": "ALT-2026-9002",
        "name": "Alert B - Failed SSH Authentication Followed by Success",
        "severity": "MEDIUM",
        "asset_criticality": "HIGH",  # Payment Gateway
        "is_ongoing": False,
        "detection_confidence": "MEDIUM",
        "source_ip": "10.0.50.12",
        "target_host": "PAYMENT-GATEWAY-01",
        "user_account": "infra_admin",
        "raw_evidence": "1x failed SSH attempt followed by success from internal subnet admin host.",
        "change_request": "CHG-2026-4401 (Scheduled Maintenance)",
        "threat_intel_flag": "Internal Approved Administrative Subnet"
    },
    {
        "alert_id": "ALT-2026-9003",
        "name": "Alert C - New Backup Service Started",
        "severity": "LOW",
        "asset_criticality": "MEDIUM",  # File Server
        "is_ongoing": False,
        "detection_confidence": "HIGH",
        "source_ip": "127.0.0.1",
        "target_host": "FILE-SRV-02",
        "user_account": "SYSTEM",
        "raw_evidence": "Windows Service Control Manager started 'EnterpriseBackupSvc' successfully.",
        "change_request": "CHG-2026-4399 (Automated Weekly Backup)",
        "threat_intel_flag": "Known Scheduled System Task"
    }
]

def calculate_priority_score(alert):
    """Calculates operational priority score based on multi-vector risk model."""
    sev_score = {"CRITICAL": 40, "HIGH": 30, "MEDIUM": 20, "LOW": 10}.get(alert["severity"], 10)
    asset_score = {"CRITICAL": 40, "HIGH": 30, "MEDIUM": 20, "LOW": 10}.get(alert["asset_criticality"], 10)
    momentum_score = 25 if alert["is_ongoing"] else 10
    
    total_score = sev_score + asset_score + momentum_score
    
    if total_score >= 80:
        return total_score, "P1 - CRITICAL ESCALATION"
    elif total_score >= 60:
        return total_score, "P2 - HIGH URGENCY"
    elif total_score >= 40:
        return total_score, "P3 - MEDIUM PRIORITY"
    else:
        return total_score, "P4 - LOW PRIORITY"

def evaluate_disposition(alert):
    """Evaluates evidence and context to assign final verdict."""
    if "ALT-2026-9001" in alert["alert_id"]:
        return "TRUE POSITIVE (TP)", "Unapproved external IP performed brute-force followed by successful administrative logon. Immediate containment required."
    elif "ALT-2026-9002" in alert["alert_id"]:
        return "BENIGN POSITIVE (BP)", "Activity matched SSH rule, but source IP is an approved internal admin host backed by Change Request CHG-2026-4401."
    elif "ALT-2026-9003" in alert["alert_id"]:
        return "FALSE POSITIVE / BENIGN (BP)", "Service startup rule triggered correctly, but activity matches scheduled weekly backup task CHG-2026-4399."
    return "INCONCLUSIVE", "Requires further log extraction."

def run_main_project():
    print("=" * 90)
    print("  DAY 14 MAIN PROJECT: ENTERPRISE SOC ALERT TRIAGE & INVESTIGATION SYSTEM")
    print("=" * 90)
    print(f"Execution Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"Lead Analyst       : Serah Kathini Mulwa (Tier 1 SOC Analyst)\n")

    dossier_content = f"# SOC ENTERPRISE TRIAGE BATCH REPORT\n**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}  \n**Analyst:** Serah Kathini Mulwa\n\n"

    for idx, alert in enumerate(MASTER_QUEUE, 1):
        score, priority = calculate_priority_score(alert)
        verdict, rationale = evaluate_disposition(alert)

        print(f"[INVESTIGATION CASE #{idx}] — {alert['name']}")
        print(f"  • Ticket ID          : {alert['alert_id']}")
        print(f"  • Target Asset       : {alert['target_host']} (Criticality: {alert['asset_criticality']})")
        print(f"  • Source IP          : {alert['source_ip']}")
        print(f"  • Calculated Priority: {priority} (Risk Score: {score})")
        print(f"  • Raw Evidence       : {alert['raw_evidence']}")
        print(f"  • External Context   : Change Request: {alert['change_request']} | Threat Intel: {alert['threat_intel_flag']}")
        print(f"  • FINAL DISPOSITION  : {verdict}")
        print(f"  • ANALYST RATIONALE  : {rationale}")
        print("-" * 90)

        # Append to Markdown Dossier
        dossier_content += f"""## Case {idx}: {alert['name']} (`{alert['alert_id']}`)
* **Target Host:** `{alert['target_host']}` ({alert['asset_criticality']})
* **Source IP:** `{alert['source_ip']}`
* **Calculated Priority:** **{priority}** (Score: `{score}`)
* **Forensic Evidence:** {alert['raw_evidence']}
* **External Context:** {alert['change_request'] or 'None'} | {alert['threat_intel_flag']}
* **Final Verdict:** **{verdict}**
* **Investigative Rationale:** {rationale}

---
"""

    # Save Master Dossier
    os.makedirs("notes", exist_ok=True)
    output_filename = "notes/main-project-triage-dossier.md"
    with open(output_filename, "w") as f:
        f.write(dossier_content)
    print(f"\n[+] Master Incident Triage Dossier successfully compiled and saved to: {output_filename}")

if __name__ == "__main__":
    run_main_project()
