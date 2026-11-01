# --- DAY 3: PYTHON FILE I/O PRACTICE ---
# Demonstrating safe file reading using context managers ('with open').

log_file_path = "sample_auth.log"

print("=== READING LOG FILES SAFELY ===")

try:
    # The 'with' statement ensures the file resource is safely closed automatically
    with open(log_file_path, "r") as file:
        line_count = 0
        for line in file:
            line_count += 1
            # .strip() removes trailing newline whitespace characters
            print(f"Line {line_count}: {line.strip()}")
            
    print(f"\nSuccessfully read {line_count} lines from {log_file_path}.")

except FileNotFoundError:
    print(f"[-] Error: Could not locate log file at {log_file_path}.")
