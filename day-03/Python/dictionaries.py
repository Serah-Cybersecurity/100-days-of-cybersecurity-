# --- DAY 3: PYTHON DICTIONARIES PRACTICE ---
# Demonstrating key-value pairs for structured security log records.

# A structured security alert record resembling JSON log data
alert_record = {
    "username": "bob",
    "source_ip": "192.0.2.50",
    "event_type": "failed_login",
    "failed_attempts": 4
}

print("=== RETRIEVING DICTIONARY VALUES ===")
# Accessing values using their specific keys
print(f"Username:    {alert_record['username']}")
print(f"Source IP:   {alert_record['source_ip']}")
print(f"Event Type:  {alert_record['event_type']}")

print("\n=== SAFE LOOKUPS WITH .get() ===")
# Using .get() prevents KeyError if a key doesn't exist
user_role = alert_record.get("role", "Unknown Role")
print(f"User Role:   {user_role}")
