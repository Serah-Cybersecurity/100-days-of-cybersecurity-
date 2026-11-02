#!/usr/bin/env python3
"""
Project: SOC Automated Alert Classification & Verdict Engine
Author: Serah Mulwa
Day 14 - Cybersecurity Journey
Purpose: Evaluates alert telemetry against threat intelligence feeds, enterprise 
         authorization lists, and log integrity metrics to assign an accurate 
         verdict (TP, FP, BP, Inconclusive) and generate audit-ready ticket notes.
"""

import json

# Enterprise Baseline Rules & Threat Intel Tables
AUTHORIZED_SCANNERS = ["10.0.50.5", "10.0.50.6"]  # Enterprise Nessus Scanners
KNOWN_THREAT_IPS = ["185.220.101.5", "45.146.164.110"]  # Known Tor Exit Nodes / C2 IPs
APPROVED_SOFTWARE_SIGNERS = ["Microsoft Corporation", "CrowdStrike Inc."]

# Test Batch of Incoming SIEM Alerts
TEST_ALERTS = [
    {
        "alert_id": "ALT-2026-8801",
        "rule_name": "SSH Brute Force Followed by Successful Authentication",
        "source_ip": "185.220.101.5",
        "target_host": "PAYMENT-GATEWAY-01",
        "user_account": "root",
        "log_telemetry_complete": True,
        "process_executed": "cat /etc/passwd",
        "signed_by": "Unsigned / Unknown"
    },
    {
        "alert_id": "ALT-2026-8802",
        "rule_name": "Suspicious PowerShell Encoded Execution",
        "source_ip": "10.0.2.15",
        "target_host": "WORKSTATION-44",
        "user_account": "SYSTEM",
        "log_telemetry_complete": True,
        "process_executed": "powershell.exe -enc Rapid7AgentUpdate",
        "signed_by": "Microsoft Corporation"
    },
    {
        "alert_id": "ALT-2026-8803",
        "rule_name": "Port Scanning and Credential Brute Force Activity",
        "source_ip": "10.0.50.5",
        "target_host": "DB-STAGE-01",
        "user_account": "nessus_svc",
        "log_telemetry_complete": True,
        "process_executed": "nessus_agent.exe",
        "signed_by": "Tenable Network Security"
    },
    {
        "alert_id": "ALT-2026-8804",
        "rule_name": "Anomalous Outbound Connection to Unknown IP",
        "source_ip": "10.0.3.88",
        "target_host": "DEV-LAPTOP-12",
        "user_account": "developer_alex",
        "log_telemetry_complete": False,  # Missing EDR Memory Logs
        "process_executed": "Unknown / Logs Corrupted",
        "signed_by": "Unknown"
    }
]

def evaluate_verdict(alert):
    """
    Evaluates telemetry against logic conditions to assign an automated verdict.
    """
    source_ip = alert.get("source_ip")
    telemetry_ok = alert.get("log_telemetry_complete", True)
    signer = alert.get("signed_by", "")
    
    # 1. Check for Missing Telemetry -> INCONCLUSIVE
    if not telemetry_ok:
        return "INCONCLUSIVE", "Missing endpoint memory/process logs. Telemetry incomplete to confirm authorization or malice."
        
    # 2. Check if Source IP is an Authorized Vulnerability Scanner -> BENIGN POSITIVE
    if source_ip in AUTHORIZED_SCANNERS:
        return "BENIGN POSITIVE (BP)", "Activity matches detection rule, but source IP belongs to an approved internal vulnerability scanner."
        
    # 3. Check for Malicious Source IP or Suspicious Post-Exploit Command -> TRUE POSITIVE
    if source_ip in KNOWN_THREAT_IPS or "cat /etc/passwd" in alert.get("process_executed", ""):
        return "TRUE POSITIVE (TP)", "Confirmed malicious activity. External threat IP matched and unauthorized post-compromise commands executed."
        
    # 4. Check if Process is Signed by Enterprise Software Vendor -> FALSE POSITIVE
    if signer in APPROVED_SOFTWARE_SIGNERS or "Rapid7" in alert.get("process_executed", ""):
        return "FALSE POSITIVE (FP)", "Detection rule flagged encoded PowerShell execution, but process is verified and digitally signed by an authorized vendor."
        
    return "INCONCLUSIVE", "Requires manual level 2 deep-dive inspection."

def run_classification_engine():
    print("=" * 85)
    print("SOC AUTOMATED ALERT CLASSIFICATION & VERDICT ENGINE")
    print("=" * 85)
    
    for alert in TEST_ALERTS:
        verdict, rationale = evaluate_verdict(alert)
        print(f"\n[+] EVALUATING TICKET: {alert['alert_id']} | Rule: '{alert['rule_name']}'")
        print(f"  • Source IP      : {alert['source_ip']}")
        print(f"  • Target Host    : {alert['target_host']}")
        print(f"  • Telemetry State: {'COMPLETE' if alert['log_telemetry_complete'] else 'CORRUPTED/MISSING'}")
        print(f"  • FINAL VERDICT  : {verdict}")
        print(f"  • RATIONALE      : {rationale}")
        print("-" * 85)

def print_closure_report(alert_id="ALT-2026-8801"):
    target_alert = next(a for a in TEST_ALERTS if a["alert_id"] == alert_id)
    verdict, rationale = evaluate_verdict(target_alert)
    
    print("\n" + "=" * 85)
    print("AUDIT-READY SOC TICKET CLOSURE & ESCALATION SUMMARY")
    print("=" * 85)
    print(f"TICKET ID             : {target_alert['alert_id']}")
    print(f"RULE TITLE            : {target_alert['rule_name']}")
    print(f"TARGET HOST           : {target_alert['target_host']}")
    print(f"SOURCE IP             : {target_alert['source_ip']}")
    print(f"FINAL CLASSIFICATION  : {verdict}")
    print("-" * 85)
    print("INVESTIGATIVE RATIONALE:")
    print(f"  {rationale}")
    print("\nRECOMMENDED NEXT ACTIONS:")
    if "TRUE POSITIVE" in verdict:
        print("  1. Immediately isolate target host PAYMENT-GATEWAY-01 from corporate network.")
        print("  2. Block IP 185.220.101.5 at edge firewall.")
        print("  3. Escalate ticket to Level 2 DFIR team for root key rotation.")
    elif "FALSE POSITIVE" in verdict:
        print("  1. Submit rule tuning request to Detection Engineering to whitelist Intune/Rapid7 hashes.")
        print("  2. Close ticket as resolved.")
    elif "BENIGN POSITIVE" in verdict:
        print("  1. Verify Nessus schedule in Change Management portal.")
        print("  2. Close ticket under Benign Positive SLA.")
    else:
        print("  1. Re-deploy Sysmon agent to restore logging telemetry.")
        print("  2. Request memory dump from endpoint administrator.")
    print("=" * 85)

if __name__ == "__main__":
    run_classification_engine()
    print_closure_report("ALT-2026-8801")
