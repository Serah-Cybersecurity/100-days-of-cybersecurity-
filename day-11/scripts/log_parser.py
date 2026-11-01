#!/usr/bin/env python3
"""
Day 11: Synthetic Security Log Parser & Triage Automation
Purpose: Load structured JSON logs, count authentication outcomes, 
         and filter security events for analytical review.
"""

import json
import sys

def load_logs(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Log file not found at {filepath}")
        sys.exit(1)

def analyze_logs(logs):
    total_events = len(logs)
    failed_logins = 0
    successful_logins = 0
    unique_ips = set()
    
    print(f"\n===== DAY 11 LOG ANALYSIS SUMMARY =====\n")
    print(f"Total Events Processed: {total_events}\n")
    
    for event in logs:
        # Track unique source IPs if present
        if "source_ip" in event:
            unique_ips.add(event["source_ip"])
            
        # Count authentication results
        if event.get("event_type") == "authentication":
            user = event.get("username", "unknown")
            ip = event.get("source_ip", "unknown")
            result = event.get("result", "unknown")
            timestamp = event.get("timestamp", "unknown")
            
            if result == "failed":
                failed_logins += 1
                print(f"[!] FAILED LOGIN: User '{user}' from IP {ip} at {timestamp}")
            elif result == "success":
                successful_logins += 1
                print(f"[+] SUCCESSFUL LOGIN: User '{user}' from IP {ip} at {timestamp}")
                
        elif event.get("event_type") == "privilege_escalation":
            user = event.get("username", "unknown")
            cmd = event.get("command", "unknown")
            print(f"[*] PRIVILEGE ESCALATION: User '{user}' executed '{cmd}'")
            
        elif event.get("event_type") == "scheduled_task":
            cmd = event.get("command", "unknown")
            print(f"[#] SCHEDULED TASK: Executed '{cmd}'")

    print(f"\n---------------------------------------")
    print(f"Summary Metrics:")
    print(f" - Failed Logins: {failed_logins}")
    print(f" - Successful Logins: {successful_logins}")
    print(f" - Unique Source IPs: {list(unique_ips)}")
    print(f"=======================================\n")

if __name__ == "__main__":
    log_path = "day-11/logs.json"
    log_data = load_logs(log_path)
    analyze_logs(log_data)
