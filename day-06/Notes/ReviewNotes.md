# Day 6 Review: Consolidating Foundations (Days 1–5)

## 1. Overview & Purpose
Before advancing into web architecture, HTTP requests, and local server hosting, this review exercises **active cognitive retrieval**. Real-world security professionals must pull foundational knowledge instantly from memory under pressure without relying on constant lookups. This document records my self-assessment, concept recalls, identified knowledge gaps, and how today's web curriculum builds upon previous learning.

---

## 2. Comprehensive Review Questionnaire & Masterclass Answers

### A. Computer Fundamentals

#### 1. What is the difference between hardware and software?
* **Definition:** Hardware is the physical, tangible machinery and electronic components of a computer; software is the intangible set of instructions (code, programs, and operating systems) that tells hardware what to do.
* **Explanation in my own words:** Hardware is what you can physically touch (chips, screens, hard drives); software is what runs inside it (code, apps, OS).
* **Example:** *Hardware:* Lenovo ThinkPad laptop chassis and CPU. *Software:* Parrot OS or Python.
* **Security relevance:** Hardware can be physically stolen or tapped; software can be injected, patched, or compromised remotely via network exploits.

#### 2. What does RAM do?
* **Definition:** Random Access Memory (RAM) is volatile, high-speed working memory that temporarily stores data and instructions currently being used by the CPU.
* **Explanation in my own words:** The computer's active scratchpad that holds open programs and data while the machine is powered on.
* **Example:** Running multiple terminal windows and virtual machines simultaneously.
* **Security relevance:** Malware often operates strictly inside RAM (fileless malware) to avoid writing files to disk where traditional antivirus scanners can detect them.

#### 3. What is the purpose of an operating system?
* **Definition:** Core system software that manages computer hardware, system resources, and provides common services for computer programs.
* **Explanation in my own words:** The central control layer that sits between physical hardware and user applications.
* **Example:** Windows or Parrot OS (Linux).
* **Security relevance:** The OS enforces privilege separation, keeping user applications isolated from kernel-level controls.

#### 4. What is the difference between a process and a file?
* **Definition:** A file is a passive collection of data stored persistently on disk; a process is an active, running instance of a program loaded into RAM and executing under OS control.
* **Explanation in my own words:** A file is dead code sitting on a hard drive; a process is that code alive and running in memory.
* **Example:** *File:* `/bin/bash` on disk. *Process:* An active shell terminal session running with a Process ID (PID).
* **Security relevance:** Files can look benign on disk, but security monitoring tools analyze active processes and parent-child process trees to catch malicious behavior.

---

### B. Networking

#### 1. What is an IP address?
* **Definition:** A unique numerical label assigned to every device connected to a computer network that uses the Internet Protocol.
* **Explanation in my own words:** The digital street address assigned to a machine so data packets know where to go.
* **Example:** `192.168.1.1` or `142.250.190.46`.
* **Security relevance:** Firewalls, ACLs, and SIEM logs rely on tracking source and destination IP addresses.

#### 2. What does a router do?
* **Definition:** A networking hardware device that forwards data packets between different computer networks.
* **Explanation in my own words:** A traffic cop that takes packets from one network and routes them toward their destination on another network.
* **Example:** Connecting a home local network to the wider internet (WAN).
* **Security relevance:** Network monitoring occurs at router choke points where traffic crosses enterprise boundaries.

#### 3. What is DNS?
* **Definition:** The hierarchical distributed naming system that translates human-readable domain names into machine-routable IP addresses.
* **Explanation in my own words:** The internet's phonebook that turns website names into IP addresses.
* **Example:** Resolving `tryhackme.com` to its server IP.
* **Security relevance:** Threat hunters analyze DNS queries to detect malware beaconing and data exfiltration via DNS tunneling.

#### 4. What is the difference between TCP and UDP?
* **Definition:** TCP is a connection-oriented, reliable transport protocol guaranteeing ordered delivery via a 3-way handshake; UDP is a connectionless, lightweight protocol without delivery guarantees.
* **Explanation in my own words:** TCP is certified mail that checks if every piece arrived; UDP is throwing paper airplanes and hoping they land.
* **Example:** *TCP:* Loading a webpage. *UDP:* Live video streaming.
* **Security relevance:** TCP handshakes can be abused for SYN flood attacks; UDP lacks handshakes and is exploited for IP spoofing and amplification DDoS.

#### 5. What is a port?
* **Definition:** A logical endpoint number (`0` to `65535`) used by the OS to direct incoming network traffic to the correct application or service.
* **Explanation in my own words:** The specific apartment door number on a computer that routes traffic to a specific program.
* **Example:** Port `22` for SSH, Port `443` for HTTPS.
* **Security relevance:** Firewalls block unauthorized destination ports to prevent external access to vulnerable internal services.

#### 6. What does HTTPS provide?
* **Definition:** Encrypted, authenticated, and integrity-protected communication between a web client and a server via TLS over TCP port 443.
* **Explanation in my own words:** A secure cryptographic wrapper around standard HTTP traffic that prevents eavesdropping.
* **Example:** Logging into a secure portal.
* **Security relevance:** While HTTPS protects user privacy from network snoopers, malware also abuses encryption to hide Command & Control (C2) traffic.

---

### C. Linux

#### 1. What does `pwd` do?
* **Definition:** Print Working Directory; outputs the absolute file path of the directory you are currently in.
* **Example:** `/media/sf_cyber-repo/100-DAYS-OF-CYBERSECURITY-From-Scratch-/day-06`.

#### 2. What does `ls` do?
* **Definition:** List; displays directory contents, permissions, and sizes when combined with flags like `ls -la`.

#### 3. What is the purpose of `ip addr`?
* **Definition:** Displays active network interfaces, IP addresses, and MAC addresses.

#### 4. What information can `ss -tuln` display?
* **Definition:** Socket Statistics; lists all active listening TCP and UDP ports numerically to audit exposed services.

---

### D. Python

#### 1. What is a variable?
* **Definition:** A named container used to store data values in memory (`port = 443`).

#### 2. What is a string?
* **Definition:** A data type representing textual characters enclosed in quotes.

#### 3. What is a list or dictionary?
* **Definition:** A list is an ordered mutable collection (`[80, 443]`); a dictionary stores key-value pairs (`{"ip": "192.0.2.10"}`).

#### 4. What is the difference between an error and an expected program result?
* **Definition:** An expected result is normal output; an error is an unexpected runtime exception (like missing files or malformed JSON) that crashes code unless handled with `try/except`.

---

### E. Investigation

#### 1. What is the difference between an observation and a conclusion?
* **Definition:** An observation is an indisputable empirical fact extracted directly from raw logs; a conclusion is a bounded operational judgment supported by verified evidence and weighed against limitations.

#### 2. Why does an unfamiliar domain not automatically prove malicious activity?
* **Definition:** Unfamiliarity or low reputation scores only reflect lack of historical context; CDNs, update servers, and APIs frequently use unfamiliar domains that require payload verification before judgment.

---

## 3. Self-Assessment Tracker

* **Green (Confident / Explained without assistance):** 
  * Computer architecture basics, OS privilege separation, IP addressing, TCP/UDP transport differences, basic Linux navigation (`pwd`, `ls`, `ip addr`, `ss -tuln`), variables/strings/lists in Python, and the observation vs. conclusion rule.
* **Yellow (Understood, require periodic reference):** 
  * Advanced socket states and exact TLS cryptographic handshake packet sequences.
* **Red (Gaps identified for continued study):** 
  * None blocking current progress; ready to proceed into Day 6 web labs.

---

## 4. Connection to Today's Work (Day 6)
The foundational networking protocols (TCP ports, IP routing, DNS resolution) and Python scripting logic reviewed above directly enable today's objective: understanding how web clients and servers communicate via HTTP requests and responses, inspecting traffic via Browser Developer Tools, and building a local Python HTTP server.
