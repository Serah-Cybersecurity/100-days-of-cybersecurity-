# Manual Analysis Notes — Day 11

## Task 1: Failed Authentications
- Total failed attempts: 3
- Source IP: 198.51.100.27
- Usernames targeted: admin, oracle, student

## Task 2: Subsequent Success
- Did a successful login occur from that IP? Yes, user 'student' logged in successfully at 09:13:22 from 198.51.100.27.
- Why review it? Multiple failures followed by a success can indicate brute-forcing.
- Why it doesn't prove compromise: A legitimate user might just be mistyping their password before getting it right.

## Task 3: Privilege-Use Inspection
- Command executed: systemctl status cron
- Is it malicious? No, it is a read-only informational command. It does not alter system files.

## Task 4: Scheduled Task Context
- What happened? The daily-report timer and service fired around 09:15.
- Is it connected to the login? No, it matches our routine system baseline in case-context.md. Temporal proximity is not causation.

## Task 5: Baseline Comparison
- What happened? User 'student' successfully logged in at 09:17 using SSH keys from 192.0.2.44.
- Baseline match? Yes, case-context.md identifies 192.0.2.44 as an approved administrative source.
