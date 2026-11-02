import json
from datetime import datetime

alert = {
    "alert_id": "ALT-2026-1104",
    "timestamp": datetime.now().isoformat(),
    "rule_name": "SSH Brute Force Followed by Successful Authentication",
    "severity": "HIGH",
    "source_ip": "192.168.1.50",
    "destination_host": "LINUX-LAB-01",
    "matched_events_count": 10,
    "user_account": "root",
    "status": "NEW"
}

print(json.dumps(alert, indent=4))
