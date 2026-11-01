# Live System Inspection Notes - Day 11

## Overview
Read-only examination of Parrot OS VM telemetry to bridge synthetic incident concepts with live Linux system operations.

## Commands Executed & Observations
1. **User Identity (`whoami`, `id`):** Verified active shell user credentials, numeric UIDs, GIDs, and supplementary group permissions determining file system access.
2. **Process Tree Inspection (`ps`):** Examined PIDs, PPIDs, and execution states. Reaffirmed that unfamiliar processes require verification rather than hasty assumptions of malice.
3. **Running Services (`systemctl`):** Listed active systemd units (e.g., `cron.service`, `NetworkManager.service`). Differentiated between managed background services and raw running processes.
4. **Listening Sockets (`ss -lnt`):** Inspected local network listeners (`127.0.0.1:52468`). Noted that listening ports require operational context (such as loopback vs. external binding) before evaluating security posture.

## Comparison: Synthetic Case vs. Live System
* **Similarities:** Both involve analyzing system services, processes, and network listeners in context, and both require recognizing telemetry gaps that demand deeper investigation.
* **Differences:** The synthetic dataset was intentionally structured with a precise, controlled sequence for learning, whereas a live operating system handles organic background tasks, updates, and applications simultaneously.

## Privacy Compliance
No raw system logs, active usernames, or external IP tables were published to maintain repository privacy and security standards.
