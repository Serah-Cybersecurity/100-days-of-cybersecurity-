# Day 3 Cybersecurity Vocabulary

## 1. Operating System
* **Definition:** Low-level system software that manages computer hardware, resources, and provides common services for computer programs.
* **Simple Explanation:** The master control program that bridges hardware and applications.
* **Example:** Parrot OS, Ubuntu, Windows 11.
* **Security Relevance:** The OS is the first line of defense; if compromised, all running applications are untrusted.

## 2. Kernel
* **Definition:** The core component of an operating system that has complete control over everything in the system.
* **Simple Explanation:** The heart of the OS that talks directly to the CPU, memory, and devices.
* **Example:** The Linux kernel.
* **Security Relevance:** Kernel-level exploits grant an attacker full system ownership (root/administrator privileges).

## 3. Shell
* **Definition:** A user interface that gives access to an operating system's services (command-line interpreter).
* **Simple Explanation:** The text interface where you type commands to tell the computer what to do.
* **Example:** Bash, Zsh.
* **Security Relevance:** Attackers use reverse shells to gain remote interactive access to compromised servers.

## 4. Terminal
* **Definition:** A text-based input/output environment that communicates with the shell.
* **Simple Explanation:** The window or console where command-line tools are executed.
* **Example:** Parrot Terminal, GNOME Terminal.
* **Security Relevance:** Where day-to-day security engineering, log analysis, and system administration occur.

## 5. Filesystem
* **Definition:** The method and data structure an OS uses to control how data is stored and retrieved.
* **Simple Explanation:** The organizational tree structure of files and folders on a hard drive.
* **Example:** Ext4, NTFS, FAT32.
* **Security Relevance:** Forensics investigators analyze the filesystem (inodes, file timestamps, deleted blocks) during incident response.

## 6. Directory
* **Definition:** A cataloging structure which contains files and other folders.
* **Simple Explanation:** A folder.
* **Example:** `/home/user/day-03/`
* **Security Relevance:** Directory permissions dictate who can read or write sensitive configuration files.

## 7. Process
* **Definition:** An instance of a computer program that is being executed by one or many threads.
* **Simple Explanation:** A living program loaded into system memory (RAM).
* **Example:** Running an instance of `python3 log_analyzer.py`.
* **Security Relevance:** Threat hunting involves inspecting running processes to detect malicious code hiding in memory.

## 8. PID (Process ID)
* **Definition:** A unique integer number assigned by the kernel to every active process.
* **Simple Explanation:** A serial number for a running program so the OS can track it.
* **Example:** PID 1 (systemd initialization process).
* **Security Relevance:** Used by engineers to target, inspect, or terminate suspicious background processes (`kill PID`).

## 9. Permission
* **Definition:** Rules determining whether a user can read, write, or execute a file or directory.
* **Simple Explanation:** Access control rules assigned to files.
* **Example:** `-rw-r--r--`
* **Security Relevance:** Misconfigured permissions often lead to unauthorized privilege escalation or data exposure.

## 10. Privilege
* **Definition:** A specialized right or immunity granted to a user or process.
* **Simple Explanation:** What level of power or access an account has.
* **Example:** Standard user vs. Root/Administrator.
* **Security Relevance:** The principle of Least Privilege restricts privileges to minimize damage if an account is compromised.

## 11. User
* **Definition:** An entity that can interact with an operating system and hold specific permissions.
* **Simple Explanation:** An individual account on a machine.
* **Example:** `user`, `root`, `bandit0`.
* **Security Relevance:** Attackers target user credentials to gain an initial foothold inside a network.

## 12. Group
* **Definition:** A collection of users sharing the same security permissions and access rights.
* **Simple Explanation:** A team or department folder access list.
* **Example:** `sudo`, `www-data`.
* **Security Relevance:** Managing access by groups makes administrative and security controls scalable.

## 13. Authentication
* **Definition:** Verifying the identity of a user, device, or system.
* **Simple Explanation:** Proving *who* you are (username, password, MFA).
* **Example:** Entering your password to log into SSH.
* **Security Relevance:** Weak authentication mechanisms are the leading entry point for cyberattacks.

## 14. Authorization
* **Definition:** Determining whether an authenticated entity has permission to access a specific resource.
* **Simple Explanation:** Proving *what* you are allowed to do.
* **Example:** A regular user getting a `Permission denied` error when trying to read `/etc/shadow`.
* **Security Relevance:** Proper authorization prevents horizontal and vertical privilege escalation.

## 15. Log
* **Definition:** An official chronological record of computer events, transactions, and system activities.
* **Simple Explanation:** A digital diary of what happened on a system.
* **Example:** `/var/log/auth.log`
* **Security Relevance:** Logs are the primary source of truth for security analysts investigating breaches.

## 16. Event
* **Definition:** Any significant occurrence in a system or network.
* **Simple Explanation:** A recorded action or occurrence.
* **Example:** A user logging in, a file being modified, a packet arriving.
* **Security Relevance:** Security tools ingest thousands of events per second to detect anomalies.

## 17. Alert
* **Definition:** A notification triggered by a security tool indicating a potential malicious event or policy violation.
* **Simple Explanation:** A red flag raised by automated security monitoring.
* **Example:** "Multiple failed logins detected from IP X."
* **Security Relevance:** Alerts drive SOC (Security Operations Center) workflows and incident response triage.

## 18. Detection
* **Definition:** The process of identifying indicators of compromise or anomalous behavior in telemetry.
* **Simple Explanation:** Spotting something suspicious in your logs or network.
* **Example:** Matching regex rules against incoming web traffic.
* **Security Relevance:** Detection is the core function of blue teams and monitoring systems.

## 19. Investigation
* **Definition:** The systematic analysis of security telemetry and evidence to determine the scope and root cause of an anomaly.
* **Simple Explanation:** Digging deeper to figure out what actually happened.
* **Example:** Tracing a failed login sequence back to a brute-force IP.
* **Security Relevance:** Remember: *Detection $\neq$ Conclusion*. Investigations turn raw alerts into verified facts.

## 20. Evidence
* **Definition:** Verifiable data collected during an investigation that supports or refutes a security hypothesis.
* **Simple Explanation:** Proof gathered from logs, disk images, or network captures.
* **Example:** Timestamps, IP addresses, and command-line execution histories.
* **Security Relevance:** Professional decisions and incident reports must be backed by solid evidence.

## 21. Automation
* **Definition:** The use of software and scripts to perform tasks without human intervention.
* **Simple Explanation:** Writing code to do repetitive work for you.
* **Example:** A Python script parsing 10,000 log lines in seconds.
* **Security Relevance:** Scales security operations to match the velocity of modern threats.

## 22. Script
* **Definition:** A file containing a sequence of instructions executed by an interpreter.
* **Simple Explanation:** A small program designed to automate a task.
* **Example:** `log_analyzer.py`
* **Security Relevance:** Used by both defenders for automation and attackers for payload delivery.

## 23. Interpreter
* **Definition:** A program that directly executes instructions written in a programming language without requiring prior compilation.
* **Simple Explanation:** The engine that reads and runs Python code line by line.
* **Example:** `python3` interpreter.
* **Security Relevance:** Understanding how interpreters execute code helps in malware reverse engineering and script auditing.

## 24. Function
* **Definition:** A self-contained block of reusable code designed to perform a specific task.
* **Simple Explanation:** A custom tool or formula you build once and call whenever needed.
* **Example:** `def evaluate_risk():`
* **Security Relevance:** Promotes modular, clean, and testable code architecture in security automation.

## 25. Loop
* **Definition:** A programming construct that repeats a block of code until a specific condition is met.
* **Simple Explanation:** Doing the same task over and over automatically.
* **Example:** `for` and `while` loops.
* **Security Relevance:** Essential for iterating over massive log files or active IP lists.

## 26. List
* **Definition:** An ordered, mutable collection of items stored in a single variable.
* **Simple Explanation:** A shopping list of data elements.
* **Example:** `suspicious_ips = [...]`
* **Security Relevance:** Used to maintain collections of IOCs (Indicators of Compromise), usernames, or file paths.

## 27. Dictionary
* **Definition:** A collection of data stored in key-value pairs.
* **Simple Explanation:** A contact list where you look up a name (key) to get a phone number (value).
* **Example:** `alert_record = {"user": "bob", "status": "failed"}`
* **Security Relevance:** Mirrors structured log payloads (JSON) generated by modern security tools and SIEMs.
