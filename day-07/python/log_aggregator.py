# Day 7 — Advanced Lists & Dictionaries Log Aggregator Exercise

# Step 1: Create a list of 5 fictional security event dictionaries
# Using official documentation-only IP ranges (RFC 5737)
security_events = [
    {
        "username": "analyst_alice",
        "event": "login_failed",
        "source_ip": "192.0.2.15"
    },
    {
        "username": "contractor_bob",
        "event": "login_success",
        "source_ip": "198.51.100.25"
    },
    {
        "username": "analyst_alice",
        "event": "login_failed",
        "source_ip": "192.0.2.15"
    },
    {
        "username": "admin_charlie",
        "event": "file_access",
        "source_ip": "203.0.113.40"
    },
    {
        "username": "guest_dave",
        "event": "login_success",
        "source_ip": "198.51.100.25"
    }
]

# Step 2: Initialize an empty dictionary to serve as our frequency counter
event_type_counts = {}

# Step 3: Loop through each event record and aggregate counts dynamically
for record in security_events:
    # Safely extract the event type, defaulting to "unknown" if missing
    current_event_type = record.get("event", "unknown")
    
    # Dynamic counter pattern: get current count (defaulting to 0) and add 1
    event_type_counts[current_event_type] = event_type_counts.get(current_event_type, 0) + 1

# Step 4: Display the final aggregated report
print("=== SECURITY EVENT AGGREGATION REPORT ===")
print(f"Total Events Processed: {len(security_events)}\n")

print("Breakdown by Event Type:")
for event_type, count in event_type_counts.items():
    print(f"  - {event_type}: {count} occurrence(s)")
print("=========================================")