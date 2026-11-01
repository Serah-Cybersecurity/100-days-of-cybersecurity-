# Day 7 — Functions Practice: Security Log Analytics Module

def count_events(events):
    """Returns the total number of event records in the dataset."""
    total_count = 0
    for event in events:
        total_count += 1
    return total_count

def count_failed_logins(events):
    """Returns the total number of failed login events."""
    failed_count = 0
    for event in events:
        # Using .get() safely handles malformed or empty dictionaries
        if event.get("event") == "login_failed":
            failed_count += 1
    return failed_count

def count_successful_logins(events):
    """Returns the total number of successful login events."""
    success_count = 0
    for event in events:
        if event.get("event") == "login_success":
            success_count += 1
    return success_count

# --- TEST DATASET ---
sample_security_events = [
    {"timestamp": "08:00:01", "username": "alice", "event": "login_failed"},
    {"timestamp": "08:00:15", "username": "bob", "event": "login_success"},
    {"timestamp": "08:01:00", "username": "alice", "event": "login_failed"},
    {"timestamp": "08:02:30", "username": "charlie", "event": "login_success"},
    {}, # Malformed empty record to test robustness
    {"timestamp": "08:03:10", "username": "admin", "event": "login_failed"}
]

# --- EXECUTION & REPORTING ---
print("=== SECURITY LOG ANALYSIS REPORT ===")
total = count_events(sample_security_events)
failures = count_failed_logins(sample_security_events)
successes = count_successful_logins(sample_security_events)

print(f"Total Events Processed: {total}")
print(f"Total Failed Logins   : {failures}")
print(f"Total Successful Logins: {successes}")
print("====================================")