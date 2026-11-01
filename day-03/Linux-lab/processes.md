# Linux Processes & Operating System Monitoring

## 1. Program vs. Process
* **Program:** A static set of instructions stored passively on a hard disk (e.g., `log_analyzer.py` sitting in a folder).
* **Process:** A living, active instance of a program loaded into system memory (`RAM`) and actively managed by the Linux kernel.

## 2. Process Observability (`ps`)
Running `ps` or `ps aux` exposes active system telemetry. Key components tracked include:
* **PID (Process ID):** A unique numerical identifier assigned by the kernel to every running process.
* **Parent/Child Hierarchy:** How parent processes spawn child processes to execute tasks.
* **Resource Consumption:** CPU and memory utilization metrics.
* **Executing User:** Which user account owns and runs the process.

## 3. Cybersecurity Relevance
Process monitoring is foundational to:
* **Malware Analysis & Threat Hunting:** Detecting malicious payloads running disguised as legitimate processes.
* **Incident Response:** Inspecting active network connections and process trees during a breach.
* **SOC Analysis:** Triaging unauthorized background execution or unexpected privilege spikes.
