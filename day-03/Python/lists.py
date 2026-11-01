# --- DAY 3: PYTHON LISTS PRACTICE ---
# Demonstrating ordered, mutable collections used for security telemetry.

# Initialize a list of suspicious IP addresses
suspicious_ips = ["192.0.2.1", "203.0.113.5", "198.51.100.42"]

print("=== ACCESSING LIST ELEMENTS ===")
# Python uses 0-based indexing
print(f"First IP in list: {suspicious_ips[0]}")
print(f"Total IPs tracked: {len(suspicious_ips)}")

print("\n=== MODIFYING LISTS ===")
# Appending a new malicious IP detected during analysis
suspicious_ips.append("10.0.0.99")
print(f"Updated IP List: {suspicious_ips}")

# Iterating over the list using a for loop
print("\nIterating through active IP blocklist:")
for ip in suspicious_ips:
    print(f"  [!] Flagged IP: {ip}")
