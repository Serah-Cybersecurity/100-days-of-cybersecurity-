# Day 10 - System Triage Methodology & Process Investigation

## 1. Environment Baseline
* **Operating System:** Parrot Security 7.4 (echo) (Debian Derivative)
* **Kernel Version:** Linux 7.0.9+parrot7-amd64 x86_64
* **User Context:** Standard unprivileged user account (`user`)
* **Deployment:** Virtual Machine running inside Oracle VirtualBox on a Windows host

## 2. Environment Verification Commands
* `whoami`: Verified active user identity as `user`.
* `pwd`: Confirmed workspace boundary (`/home/user`).
* `uname -a`: Extracted kernel architecture and build details.
* `cat /etc/os-release`: Parsed OS distribution metadata.

## 3. Process Investigation & Forensic Queries
* **Dynamic Monitoring (`top` / `htop`):** Observed live CPU/Memory utilization to identify real-time resource spikes.
* **Shell PID Identification:** Executed `echo $$` to obtain the PID of the active interactive shell (`1872`).
* **Targeted Attribute Query:** Executed `ps -p "$$" -o pid,ppid,user,stat,etime,comm` to isolate attributes for PID `1872` (`PPID: 1864`, `USER: user`, `STAT: Ss`, `ELAPSED: 10:34`, `COMMAND: bash`).
* **Kernel Abstraction (`/proc`):** Checked directory existence for `/proc/1872/` using `ls -ld "/proc/$$"`, confirming that the kernel dynamically exposes live process metadata in RAM (`dr-xr-xr-x`).

## Portfolio Security & Data Sanitization Rules

* **Information Redaction:** Never expose raw internal IP addresses, sensitive hostnames, private API tokens, or personal credentials in public repositories.
* **Evidence-Driven Analysis:** Record process observations factually (e.g., *"unidentified at this stage"*) rather than making hasty security assumptions without behavioral evidence.
* **Unprivileged Baseline:** Conduct initial host triage under standard user permissions to evaluate visibility before requesting administrative privilege escalation.
