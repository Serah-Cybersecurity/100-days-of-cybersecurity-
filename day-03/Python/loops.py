# --- DAY 3: PYTHON LOOPS PRACTICE ---
# Demonstrating 'for' loops over collections and 'while' loops with condition tracking.

print("=== 1. FOR LOOP PRACTICE ===")
users = ["alice", "bob", "charlie"]

# Iterating through a list of usernames
for user in users:
    print(f"Checking access for user: {user}")

print("\n=== 2. WHILE LOOP & THRESHOLD PRACTICE ===")
# Using a while loop to track attempts and prevent infinite loops
attempts = 0
max_attempts = 3

while attempts < max_attempts:
    print(f"Authentication attempt {attempts + 1} in progress...")
    attempts += 1  # Crucial step: increments counter to eventually terminate the loop

print("Loop terminated successfully. Max attempts reached.")
