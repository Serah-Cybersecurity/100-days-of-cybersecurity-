#!/usr/bin/env python3
"""
Project: SOC Dynamic Alert Queue Prioritizer
Author: Serah Mulwa
Day 14 - Cybersecurity Journey
Purpose: Solves alert fatigue by calculating operational Priority Scores (P1-P4) 
         based on Severity, Asset Criticality, Threat Momentum, and Confidence.
"""

import json

# Sample Incoming Unsorted SIEM Alert Queue
UNSORTED_ALERT_QUEUE = [
    {
        "alert_id": "ALT-2026-001",
        "rule_name": "PowerShell Script Execution with Encoded Command",
        "severity": "HIGH",
        "target_host": "DEV-SANDBOX-04",
        "asset_criticality": "LOW",  # Disposable Lab Machine
        "is_ongoing": False,
        "detection_confidence": "HIGH",
        "source_ip": "10.0.99.15"
    },
    {
        "alert_id": "ALT-2026-002",
        "rule_name": "SSH Brute Force Followed by Successful Authentication",
        "severity": "MEDIUM",
        "target_host": "PAYMENT-GATEWAY-01",
        "asset_criticality": "CRITICAL",  # Crown Jewel Asset
        "is_ongoing": True,
        "detection_confidence": "HIGH",
        "source_ip": "192.168.1.50"
    },
    {
        "alert_id": "ALT-2026-003",
        "rule_name": "Mimikatz LSASS Memory Dump Attempt",
        "severity": "CRITICAL",
        "target_host": "DC-01.corp.local",
        "asset_criticality": "CRITICAL",  # Domain Controller
        "is_ongoing": True,
        "detection_confidence": "HIGH",
        "source_ip": "10.0.1.5"
    },
    {
        "alert_id": "ALT-2026-004",
        "rule_name": "Multiple Port Scanning Activity",
        "severity": "LOW",
        "target_host": "PRINT-SERVER-02",
        "asset_criticality": "LOW",
        "is_ongoing": False,
        "detection_confidence": "MEDIUM",
        "source_ip": "10.0.4.88"
    },
    {
        "alert_id": "ALT-2026-005",
        "rule_name": "Anomalous Outbound Data Transfer",
        "severity": "HIGH",
        "target_host": "WORKSTATION-88",
        "asset_criticality": "MEDIUM",  # Standard User PC
        "is_ongoing": False,
        "detection_confidence": "LOW",
        "source_ip": "10.0.2.110"
    }
]

def calculate_priority_score(alert):
    """
    Calculates a numerical risk weight score based on multiple SOC contextual vectors.
    """
    score = 0
    
    # 1. Base Severity Weight
    severity_weights = {
        "CRITICAL": 40,
        "HIGH": 30,
        "MEDIUM": 20,
        "LOW": 10
    }
    score += severity_weights.get(alert["severity"].upper(), 10)
    
    # 2. Asset Criticality Weight
    asset_weights = {
        "CRITICAL": 35,  # Crown Jewels (DB, Domain Controller, Payment Gateway)
        "MEDIUM": 15,    # Standard Workstations / File Shares
        "LOW": 5        # Isolated Test/Dev/Print Servers
    }
    score += asset_weights.get(alert["asset_criticality"].upper(), 5)
    
    # 3. Threat Momentum (Is the attack active RIGHT NOW?)
    if alert.get("is_ongoing", False):
        score += 20
        
    # 4. Rule Fidelity / Confidence Weight
    confidence_weights = {
        "HIGH": 10,
        "MEDIUM": 5,
        "LOW": 0
    }
    score += confidence_weights.get(alert["detection_confidence"].upper(), 0)
    
    # 5. Map Numerical Score to Operational Priority Category (P1 - P4)
    if score >= 80:
        priority_label = "P1 - CRITICAL"
    elif score >= 60:
        priority_label = "P2 - HIGH"
    elif score >= 35:
        priority_label = "P3 - MEDIUM"
    else:
        priority_label = "P4 - LOW"
        
    return score, priority_label

def prioritize_queue(raw_queue):
    print("=" * 80)
    print("SOC AUTOMATED ALERT QUEUE PRIORITIZER & RISK MATRIX ENGINE")
    print("=" * 80)
    
    processed_queue = []
    for alert in raw_queue:
        score, priority_label = calculate_priority_score(alert)
        alert_copy = alert.copy()
        alert_copy["risk_score"] = score
        alert_copy["calculated_priority"] = priority_label
        processed_queue.append(alert_copy)
        
    # Sort descending by risk_score
    sorted_queue = sorted(processed_queue, key=lambda x: x["risk_score"], reverse=True)
    
    print("\n[+] PRIORITIZED QUEUE ORDER (HIGHEST RISK TO LOWEST RISK):\n")
    print(f"{'RANK':<5} {'PRIORITY':<15} {'SCORE':<7} {'SEVERITY':<10} {'TARGET ASSET':<22} {'RULE TITLE'}")
    print("-" * 80)
    
    for rank, alert in enumerate(sorted_queue, 1):
        print(f"{rank:<5} {alert['calculated_priority']:<15} {alert['risk_score']:<7} {alert['severity']:<10} {alert['target_host']:<22} {alert['rule_name']}")
        
    print("-" * 80)
    
    print("\n[+] DETAILED OPERATIONAL JUSTIFICATION FOR TOP TICKET:")
    top_ticket = sorted_queue[0]
    print(f"  • Ticket ID         : {top_ticket['alert_id']}")
    print(f"  • Calculated Priority: {top_ticket['calculated_priority']} (Score: {top_ticket['risk_score']})")
    print(f"  • Target Host       : {top_ticket['target_host']} (Criticality: {top_ticket['asset_criticality']})")
    print(f"  • Threat Momentum   : {'ACTIVE / ONGOING' if top_ticket['is_ongoing'] else 'HISTORICAL'}")
    print(f"  • Analyst Action    : IMMEDIATE P1 ESCALATION REQUIRED. DO NOT DELAY.")
    print("=" * 80)

if __name__ == "__main__":
    prioritize_queue(UNSORTED_ALERT_QUEUE)
