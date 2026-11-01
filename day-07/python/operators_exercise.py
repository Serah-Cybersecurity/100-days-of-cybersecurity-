# Day 7 — Operators and Conditional Logic Exercise

# Define our baseline threshold
threshold = 5

print("--- SCENARIO 1: Count is BELOW the threshold ---")
failed_count_1 = 3
print(f"Failed logins: {failed_count_1} | Threshold: {threshold}")

# Compare count with threshold
if failed_count_1 > threshold:
    print("ALERT: Failed logins exceed threshold!")
elif failed_count_1 == threshold:
    print("NOTICE: Failed logins have reached the exact threshold limit.")
else:
    print("STATUS: Normal activity. Failed logins are below threshold.")


print("\n--- SCENARIO 2: Count is EQUAL TO the threshold ---")
failed_count_2 = 5
print(f"Failed logins: {failed_count_2} | Threshold: {threshold}")

if failed_count_2 > threshold:
    print("ALERT: Failed logins exceed threshold!")
elif failed_count_2 == threshold:
    print("NOTICE: Failed logins have reached the exact threshold limit.")
else:
    print("STATUS: Normal activity. Failed logins are below threshold.")


print("\n--- SCENARIO 3: Count is ABOVE the threshold ---")
failed_count_3 = 9
print(f"Failed logins: {failed_count_3} | Threshold: {threshold}")

if failed_count_3 > threshold:
    print("ALERT: Failed logins exceed threshold! Investigate source IP.")
elif failed_count_3 == threshold:
    print("NOTICE: Failed logins have reached the exact threshold limit.")
else:
    print("STATUS: Normal activity. Failed logins are below threshold.")