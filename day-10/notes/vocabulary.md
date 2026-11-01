# Day 10 - Linux Triage & Process Investigation Vocabulary

## 1. Core Operating System & Process Concepts
* **Process:** An instance of a computer program that is currently being executed by the operating system kernel, assigned a unique Process ID (PID), memory space, and security context.
* **PID (Process ID):** A unique positive integer assigned by the operating system kernel to identify and track every active process.
* **PPID (Parent Process ID):** The Process ID of the process that spawned or created the current process, establishing parent-child process hierarchies.
* **Daemon:** A background service process that runs without direct user interaction, usually initiated at system boot to handle recurring system tasks (e.g., `sshd`, `cron`, `rsyslog`).
* **Kernel:** The core foundational component of the Linux operating system that acts as an interface between user-space applications and physical hardware.

## 2. Process Inspection & Monitoring Tools
* **`ps` (Process Status):** A command-line utility used to generate a static, point-in-time snapshot of active processes running on the system.
* **`top` / `htop`:** Interactive terminal utilities used for real-time, dynamic monitoring of system resource utilization, CPU loads, memory usage, and active processes.
* **`/proc`:** A pseudo-filesystem maintained by the Linux kernel that exposes runtime system and process information as hierarchical text files.
* **`kill` / `pkill`:** Signals sent to processes to request termination, stop execution, or modify runtime behavior.

## 3. Services & Persistence Mechanisms
* **Service:** A managed background application or daemon configured to provide ongoing operating system functions or network services.
* **`systemd`:** The modern system and service manager used across major Linux distributions to initialize the operating system, manage daemons, and control system state.
* **`systemctl`:** The primary command-line control interface used to examine, start, stop, enable, or disable `systemd` services and timers.
* **Active vs. Enabled:** 
  * *Active:* The service is currently running in memory.
  * *Enabled:* The service is configured to start automatically upon system boot.
* **Cron / Crontab:** A time-based job scheduler daemon (`cron`) and configuration utility (`crontab`) used to execute automated commands or scripts at scheduled intervals.
* **Systemd Timers:** A modern alternative to cron managed directly by `systemd`, offering calendar-based and monotonic scheduling triggers.

## 4. Network & Logging Terminology
* **Socket:** An endpoint for bidirectional inter-process communication across a computer network, defined by an IP address and port number.
* **`ss` (Socket Statistics):** A modern command-line utility used to dump socket statistics, inspect listening TCP/UDP ports, and analyze network connections.
* **Journal:** The centralized binary logging architecture managed by `systemd` (`journalctl`) that collects kernel messages, service logs, and system events.
* **Log Priority:** Severity levels used to classify log entries (ranging from `emerg` and `err` to `warning` and `info`).

## 5. Security Engineering & Incident Response Principles
* **Data Minimization:** The security principle of collecting only the specific information required for an operational task while omitting sensitive or unnecessary personal telemetry.
* **Read-Only Scope:** An operational constraint where a tool or script exclusively observes and records system states without altering configurations, permissions, or files.
* **Observation vs. Interpretation:** 
  * *Observation:* Empirical, verifiable data retrieved directly from command output or logs.
  * *Interpretation:* Analytical reasoning or working hypotheses derived from evaluating observations against context.
* **Baseline:** A documented record of normal, expected system behavior, resource utilization, and configurations used as a reference point to detect anomalies.
