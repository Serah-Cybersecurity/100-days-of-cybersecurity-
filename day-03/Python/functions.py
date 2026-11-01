# --- DAY 3: PYTHON FUNCTIONS PRACTICE ---
# Demonstrating modular, reusable logic for security triage.

def evaluate_risk(failed_count):
    """
    Evaluates failure count against threshold triage rules
    and returns a standardized risk classification string.
    """
    if failed_count == 0:
        return "Clean - Low Concern"
    elif failed_count <= 2:
        return "Low Concern"
    elif failed_count <= 4:
        return "Review Recommended"
    else:
        return "HIGH PRIORITY FOR INVESTIGATION"

print("=== TESTING TRIAGE FUNCTIONS ===")
# Testing our modular function with different input arguments
users_tested = {"alice": 1, "bob": 4, "dave": 6}

for username, failures in users_tested.items():
    triage_result = evaluate_risk(failures)
    print(f"User: {username:<10} | Failures: {failures} | Triage Status: {triage_result}")
