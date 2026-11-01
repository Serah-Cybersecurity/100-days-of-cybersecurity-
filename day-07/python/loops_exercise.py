# Day 7 — Loops and Event Counting Exercise

# Step 1: Create a list containing five fictional event names
security_events = [
    "login_success",
    "login_failed",
    "file_access",
    "login_failed",
    "logout"
]

print("--- PART A: Printing Each Event ---")
# Step 2: Write a loop that prints each event sequentially
for event_name in security_events:
    print(f"Observed event in stream: {event_name}")


print("\n--- PART B: Counting Specific Matching Records ---")
# Step 3: Modify the program to count only 'login_failed' events
failed_target_count = 0

for event_name in security_events:
    if event_name == "login_failed":
        failed_target_count += 1

print(f"Total target 'login_failed' events found: {failed_target_count}")