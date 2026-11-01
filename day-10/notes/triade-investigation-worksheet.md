# Day 10 - Linux Triage Method & Analytical Investigation Worksheet

## 1. Objective
*What question am I trying to answer?* (e.g., Are the active background services on this host consistent with a standard, uncompromised Parrot OS development environment?)

## 2. Scope
*Which machine or lab environment am I examining?* (e.g., Local Parrot OS Virtual Machine running on VirtualBox).

## 3. Command
*What exact command did I execute?* (e.g., `systemctl list-units --type=service --state=running --no-pager`)

## 4. Observation
*What did the command actually show?* (e.g., Listed active running services including `cron.service`, `NetworkManager.service`, and an unfamiliar service named `cpupower-gui-helper.service`).

## 5. Interpretation
*What does that output suggest?* (e.g., The presence of an unfamiliar power-management helper service suggests potential power-scaling daemons, but its exact function requires validation).

## 6. Alternative explanations
*What else could explain the observation?* (e.g., It could be a pre-installed desktop utility package bundled with the Parrot OS distribution for laptop CPU frequency scaling).

## 7. Evidence needed
*What additional information would help establish the facts?* (e.g., Inspecting package ownership via `dpkg -S`, reviewing unit file paths under `/lib/systemd/system/`, and checking corresponding journal logs).

## 8. Limitations
*What can this command not establish?* (e.g., `systemctl` shows current runtime state but does not prove whether the binary executing behind the service has been altered or tampered with).

## 9. Conclusion
*What can I reasonably conclude at this stage?* (e.g., The service is present in memory and native to the OS package ecosystem. Further inspection confirms it is a legitimate power management utility; no indicator of compromise detected).
