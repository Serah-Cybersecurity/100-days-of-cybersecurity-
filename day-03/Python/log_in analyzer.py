# --- DAY 3 PROJECT: LOG ANALYZER ---
# Parses a log file, counts total entries, and flags specific security terms.

log_path = "sample_auth.log"
target_keyword = "Failed"

print(f"=== ANALYZING LOG FILE: {log_path} ===")

try:
    total_lines = 0
    matched_events = 0

    with open(log_path, "r") as f:
        for line in f:
            total_lines += 1
            if target_keyword in line:
                matched_events += 1
                print(f"[!] Flagged Event (Line {total_lines}): {line.strip()}")

    print(f"\nScan Complete. Total lines: {total_lines} | Flagged '{target_keyword}' events: {matched_events}")

except FileNotFoundError:
    print(f"[-] Note: {log_path} not found. Creating a mock run for demonstration.")
    print("[!] Simulated Log Analysis: 3 failed login attempts detected.")
