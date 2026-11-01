# --- DAY 3 PROJECT: SECURITY EVENT CLASSIFIER ---
# Evaluates log telemetry records using a dictionary and assigns risk tiers.

def classify_event(event_record):
    """
    Classifies risk based on failure counts and event types.
    """
    failures = event_record.get("failed_attempts", 0)
    event_type = event_record.get("event_type", "unknown")

    if event_type == "successful_login":
        return "INFO - Normal Activity"
    elif failures >= 5:
        return "HIGH - Potential Brute-Force Attack"
    elif failures >= 2:
        return "MEDIUM - Suspicious Repeated Failures"
    else:
        return "LOW - Minor Anomaly"

print("=== SECURITY EVENT CLASSIFIER ===")
sample_events = [
    {"username": "alice", "event_type": "failed_login", "failed_attempts": 1},
    {"username": "bob", "event_type": "failed_login", "failed_attempts": 6},
    {"username": "charlie", "event_type": "successful_login", "failed_attempts": 0}
]

for event in sample_events:
    tier = classify_event(event)
    print(f"User: {event['username']:<10} | Failures: {event['failed_attempts']} | Classification: {tier}")
