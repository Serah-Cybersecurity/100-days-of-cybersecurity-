# Day 7 — Conditional Categorization & Boundary Testing Exercise

def categorize_logins(failed_count):
    """Categorizes failed login counts based on security thresholds."""
    print(f"Testing failed_count value: {failed_count}")
    
    if failed_count == 0:
        print("  -> Status: No failed logins recorded.")
    elif failed_count >= 1 and failed_count <= 4:
        print("  -> Status: Below the review threshold (Normal activity).")
    else:
        print("  -> ALERT: 5 or more failed logins! Review the event group.")
    print("-" * 50)

# --- BOUNDARY TESTING EXECUTION ---
print("=== STARTING BOUNDARY TESTS ==-\n")

# Test 1: Lower absolute boundary (0)
categorize_logins(0)

# Test 2: Lower range threshold boundary (1)
categorize_logins(1)

# Test 3: Upper range threshold boundary (4)
categorize_logins(4)

# Test 4: Exact threshold trigger boundary (5)
categorize_logins(5)

# Test 5: Upper boundary exceeding threshold (6)
categorize_logins(6)

print("=== BOUNDARY TESTING COMPLETE ===")