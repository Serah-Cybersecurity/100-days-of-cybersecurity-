#!/usr/bin/env python3
"""
Project: SOC Alert Metadata Parser & Ingestion Latency Calculator
Author: Serah Mulwa
Day 14 - Cybersecurity Journey
Purpose: Demonstrates automated alert property extraction and ingestion lag analysis.
"""

import json
from datetime import datetime

# Sample incoming SIEM Alert Object (Simulating JSON payload from Elasticsearch/Splunk)
RAW_ALERT_JSON = """
{
    "alert_id": "ALT-2026-1104-8834",
    "rule_name": "SSH Brute Force Followed by Successful Authentication",
    "severity": "HIGH",
    "status": "In Progress",
    "assignee": "Tier 1 Analyst",
    "target_host": "LINUX-LAB-01",
    "user_account": "root",
    "source_ip": "192.168.1.50",
    "matched_events_count": 10,
    "event_time": "2026-11-01T18:42:38Z",
    "alert_time": "2026-11-01T18:50:03Z",
    "mitre_attack": "T1110.001 - Password Guessing"
}
"""

def parse_and_analyze_alert(json_str):
    print("=" * 70)
    print("SOC ALERT METADATA PARSER & INGESTION LATENCY ANALYZER")
    print("=" * 70)
    
    # 1. Parse JSON payload
    alert = json.loads(json_str)
    
    print("\n[+] EXTRACTED ALERT PROPERTIES:")
    print(f"  • Alert ID           : {alert['alert_id']}")
    print(f"  • Rule Title         : {alert['rule_name']}")
    print(f"  • Severity           : {alert['severity']}")
    print(f"  • Target Asset       : {alert['target_host']}")
    print(f"  • User Account       : {alert['user_account']}")
    print(f"  • Source IP          : {alert['source_ip']}")
    print(f"  • Event Count        : {alert['matched_events_count']}")
    print(f"  • MITRE Mapping      : {alert['mitre_attack']}")

    # 2. Extract Timestamps and Calculate Ingestion Latency Delta
    # Formats: ISO 8601 strings ending in 'Z'
    event_dt = datetime.strptime(alert['event_time'], "%Y-%m-%dT%H:%M:%SZ")
    alert_dt = datetime.strptime(alert['alert_time'], "%Y-%m-%dT%H:%M:%SZ")
    
    delta = alert_dt - event_dt
    latency_minutes = delta.total_seconds() / 60.0

    print("\n[+] FORENSIC TIMELINE & LATENCY ANALYSIS:")
    print(f"  • Event Time (Endpoint): {alert['event_time']}")
    print(f"  • Alert Time (SIEM)    : {alert['alert_time']}")
    print(f"  • Ingestion Latency    : {latency_minutes:.2f} minutes ({delta.total_seconds()} seconds)")
    
    if latency_minutes > 5.0:
        print("  • WARNING: High ingestion lag detected! Check SIEM forwarder queue and network bandwidth.")
    else:
        print("  • STATUS: Ingestion pipeline performance is within normal operational thresholds.")
    
    print("=" * 70)

if __name__ == "__main__":
    parse_and_analyze_alert(RAW_ALERT_JSON)
