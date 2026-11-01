# Day 7 — Variables and Data Types Practical Script

# 1. String variable (Fictional Username)
username = "analyst_serah"
print("Username:", username, "| Type:", type(username))

# 2. String variable (Fictional Event Type)
event_type = "login_failed"
print("Event Type:", event_type, "| Type:", type(event_type))

# 3. Integer variable (Event Count)
failed_count = 7
print("Failed Count:", failed_count, "| Type:", type(failed_count))

# 4. Boolean variable (Account Status)
account_locked = False
print("Account Locked:", account_locked, "| Type:", type(account_locked))

# 5. List variable (Network Protocols)
protocols = ["TCP", "UDP", "ICMP", "HTTPS"]
print("Protocols List:", protocols, "| Type:", type(protocols))
print("First Protocol in List:", protocols[0])

# 6. Dictionary variable (Structured Security Event Record)
security_event = {
    "timestamp": "2026-03-30 08:30:00",
    "username": "analyst_serah",
    "event": "login_failed",
    "source_ip": "192.0.2.50"
}
print("Security Event Dictionary:", security_event, "| Type:", type(security_event))
print("Event Log Action:", security_event["event"])