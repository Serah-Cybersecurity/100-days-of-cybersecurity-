# --- DAY 3 PROJECT: LOGIN COUNTER ---
# Aggregates authentication failures per user using a dictionary frequency map.

print("=== LOGIN FAILURE COUNTER ===")

# Simulated stream of authentication failure events
auth_logs = [
    "Failed password for invalid user admin from 192.0.2.1",
    "Failed password for root from 192.0.2.1",
    "Failed password for admin from 192.0.2.1",
    "Accepted publickey for ubuntu from 192.0.2.50",
    "Failed password for admin from 192.0.2.1"
]

failure_counts = {}

for log in auth_logs:
    if "Failed password" in log:
        # Simple parsing logic to extract targeted username
        parts = log.split("for ")
        if len(parts) > 1:
            target_info = parts[1].split(" from")[0]
            # Increment frequency counter in dictionary
            failure_counts[target_info] = failure_counts.get(target_info, 0) + 1

print("\nAggregated Failure Frequencies by Target Account:")
for account, count in failure_counts.items():
    print(f"  Target: {account:<15} | Failed Attempts: {count}")
