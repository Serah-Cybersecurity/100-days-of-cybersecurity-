# Day 7 - Comprehensive Knowledge Review & Self-Assessment Report

## 1. Executive Summary & Review Objectives
Prior to initiating Python programming and log-parser development on Day 7, this review systematically validates foundational knowledge acquired during Days 1–6. Active recall and self-assessment prevent "illusion of competence" and ensure a seamless transition into security automation and script analysis.

---

## 2. In-Depth Technical Review

### SECTION A: COMPUTER FUNDAMENTALS

#### 1. What is the difference between hardware and software?
* **Detailed Explanation:** Hardware comprises the physical, tangible electronics and mechanical components of a computer system (e.g., Central Processing Unit [CPU], Motherboard, Random Access Memory [RAM], Hard Disk Drives [HDD]/Solid State Drives [SSD]). Software is the intangible collection of instructions, code, operating systems, and programs that direct hardware on what operations to execute.
* **Real-World Example:** The physical SSD inside a server is hardware; the database management system (e.g., PostgreSQL) writing records to that drive is software.
* **Security Relevance:** Security analysts must differentiate between physical layer attacks (e.g., malicious USB Rubber Ducky insertion or hardware keyloggers) and software vulnerabilities (e.g., buffer overflows or unpatched application bugs).
* **Job Market Context:** Incident Responders and Forensic Analysts determine whether an intrusion involved physical hardware tampering or software exploitation during post-incident containment.

#### 2. What is an operating system (OS)?
* **Detailed Explanation:** An operating system is the core system software that manages computer hardware resources, coordinates running programs, and provides common services for application software. The core kernel acts as an intermediary between user applications and low-level hardware.
* **Real-World Example:** Windows 11, Parrot OS, Ubuntu Linux, and macOS.
* **Security Relevance:** The operating system enforces privilege boundaries (e.g., standard user vs. Root/Administrator access), manages process isolation, enforces access control lists (ACLs) on files, and generates system audit logs.
* **Job Market Context:** System Administrators and SOC Analysts audit OS event logs (e.g., Windows Event ID 4624/4625 or Linux `/var/log/auth.log`) to identify unauthorized access or privilege escalation attempts.

#### 3. What is the difference between RAM and storage?
* **Detailed Explanation:** 
  * **RAM (Random Access Memory):** High-speed, volatile memory used by the CPU to read and write active operational data currently in use by running processes. When power is removed, all data stored in RAM is immediately lost.
  * **Storage (SSD/HDD):** Non-volatile, long-term secondary memory designed to store files, operating system binaries, and user data permanently across reboots.
* **Real-World Example:** When writing a Python script in VS Code, the unsaved code resides temporarily in RAM; when you press `Ctrl + S`, the file is written permanently to storage.
* **Security Relevance:** Advanced threat actors deploy fileless malware that executes exclusively in RAM to bypass traditional disk-based antivirus scanners.
* **Job Market Context:** Digital Forensics and Incident Response (DFIR) specialists perform "live memory acquisition" (RAM dumping) to capture active cryptographic keys, decrypted payloads, and active network sockets that do not exist on disk storage.

#### 4. What is a process?
* **Detailed Explanation:** A process is an active instance of an executable computer program being executed by one or more threads within the CPU. It contains its own allocated memory space, process identifier (PID), security context, and file descriptors.
* **Real-World Example:** Launching PowerShell spawns a `powershell.exe` process with a unique PID assigned by the Windows task manager.
* **Security Relevance:** Attackers frequently inject malicious code into legitimate, trusted operating system processes (e.g., `lsass.exe` or `svchost.exe`) to hide their activities from monitoring tools.
* **Job Market Context:** Threat Hunters monitor process creation events (e.g., Sysmon Event ID 1) to identify suspicious parent-child process relationships (such as Word spawning `cmd.exe`).

---

### SECTION B: NETWORKING FUNDAMENTALS

#### 1. What is an IP address?
* **Detailed Explanation:** An Internet Protocol (IP) address is a unique numerical logical identifier assigned to every network interface connected to a computer network using the Internet Protocol. IPv4 uses 32-bit dotted-decimal addresses (e.g., `192.0.2.1`), while IPv6 uses 128-bit hexadecimal strings.
* **Real-World Example:** `127.0.0.1` is the IPv4 loopback address; `8.8.8.8` is a public IPv4 address assigned to Google's primary DNS resolver.
* **Security Relevance:** IP addresses serve as primary network indicators of compromise (IOCs) when blocking malicious traffic at perimeter firewalls.
* **Job Market Context:** SOC Analysts analyze firewall logs to identify ingress port scans originating from unauthorized public IP blocks.

#### 2. What does DNS do?
* **Detailed Explanation:** The Domain Name System (DNS) is a decentralized hierarchical database protocol that translates human-readable domain hostnames (e.g., `github.com`) into machine-routable IP addresses (e.g., `140.82.121.4`) over UDP/TCP port 53.
* **Real-World Example:** Typing `http://localhost:8000` uses local resolution to route to `127.0.0.1`.
* **Security Relevance:** Attackers utilize DNS for Command and Control (C2) beaconing, DNS tunneling (data exfiltration over DNS queries), and domain spoofing.
* **Job Market Context:** Network Security Engineers monitor DNS query logs to identify internal hosts making queries to newly registered or high-risk domain names.

#### 3. What is the difference between TCP and UDP?
* **Detailed Explanation:**
  * **TCP (Transmission Control Protocol):** A connection-oriented, highly reliable transport layer protocol that establishes connections using a 3-Way Handshake (`SYN` -> `SYN-ACK` -> `ACK`), guarantees in-order packet delivery, and manages flow control.
  * **UDP (User Datagram Protocol):** A connectionless, lightweight transport layer protocol that transmits packets ("datagrams") without establishing a pre-connection handshake, offering no delivery or ordering guarantees in exchange for low latency.
* **Real-World Example:** Web browsing (HTTP/HTTPS) uses TCP; live voice calls, video streaming, and DNS queries primarily use UDP.
* **Security Relevance:** TCP connections leave clear session state logs, whereas UDP flood attacks are frequently leveraged in Distributed Denial of Service (DDoS) amplification vectors.
* **Job Market Context:** Network Analysts use Wireshark to reconstruct full TCP streams during packet analysis to extract transferred malicious files.

#### 4. What is a port?
* **Detailed Explanation:** A port is a 16-bit numerical endpoint identifier (ranging from `0` to `65535`) allocated by the operating system to route incoming and outgoing network traffic to specific applications or network services.
* **Real-World Example:** HTTP uses Port 80, HTTPS uses Port 443, SSH uses Port 22, and DNS uses Port 53.
* **Security Relevance:** Unused or unmonitored open ports represent an expanded attack surface for unauthorized network entry.
* **Job Market Context:** Vulnerability Management Analysts execute Nmap network scans to map active open ports and identify outdated service versions.

#### 5. What does HTTPS protect?
* **Detailed Explanation:** HTTPS (Hypertext Transfer Protocol Secure) protects HTTP communications in transit by encrypting network packets and authenticating server identity using Transport Layer Security (TLS). It guarantees confidentiality, data integrity, and server authentication.
* **Real-World Example:** Transmitting credit card details over an encrypted HTTPS connection prevents local Wi-Fi eavesdroppers from viewing cleartext credentials.
* **Security Relevance:** HTTPS stops Man-in-the-Middle (MitM) packet sniffing attacks on local network segments.
* **Job Market Context:** Application Security Engineers enforce HTTP Strict Transport Security (HSTS) headers to prevent protocol downgrade attacks.

---

### SECTION C: WEB FUNDAMENTALS

#### 1. What is an HTTP request?
* **Detailed Explanation:** An HTTP request is a formatted text message transmitted by a client to a server requesting a resource or action. It contains a request line (Method, URI Path, HTTP Version), request headers (metadata), and an optional request body payload.
* **Real-World Example:** `GET /index.html HTTP/1.1` sent by a web browser to retrieve a homepage.
* **Security Relevance:** Web application attacks (XSS, SQLi, Directory Traversal) are delivered directly inside HTTP request URIs, headers, or body parameters.
* **Job Market Context:** Web Application Penetration Testers manipulate raw HTTP requests using tools like Burp Suite to test input sanitization logic.

#### 2. What is an HTTP response?
* **Detailed Explanation:** An HTTP response is a formatted text message returned by a web server to a client in response to a request. It contains a status line (HTTP Version, Status Code, Reason Phrase), response headers (server metadata, security policies), and an optional response body payload.
* **Real-World Example:** `HTTP/1.1 200 OK` followed by HTML code bytes.
* **Security Relevance:** Response headers dictate browser security boundaries (e.g., Content Security Policy and cookie attributes).
* **Job Market Context:** Security Auditors verify that web applications return proper error responses without exposing sensitive internal stack traces.

#### 3. What is the difference between HTML and CSS?
* **Detailed Explanation:**
  * **HTML (HyperText Markup Language):** The structural markup language used to define elements, content hierarchy, and semantic layout of a web document.
  * **CSS (Cascading Style Sheets):** The stylesheet language used to format visual presentation, colors, typography, margins, and layout rules for HTML elements.
* **Real-World Example:** `<p>Hello World</p>` defines a paragraph tag in HTML; `p { color: red; }` styles that paragraph text red using CSS.
* **Security Relevance:** Improperly encoded user input rendered in HTML DOM elements leads to Reflected or Stored Cross-Site Scripting (XSS).
* **Job Market Context:** Security QA Testers verify that user input fields render safely without executing arbitrary HTML/JavaScript tags.

#### 4. What is a status code?
* **Detailed Explanation:** A 3-digit numeric indicator returned in an HTTP response signaling the outcome category of a client's request:
  * `1xx`: Informational
  * `2xx`: Success (e.g., `200 OK`)
  * `3xx`: Redirection (e.g., `301 Moved Permanently`)
  * `4xx`: Client Error (e.g., `401 Unauthorized`, `403 Forbidden`, `404 Not Found`)
  * `5xx`: Server Error (e.g., `500 Internal Server Error`, `503 Service Unavailable`)
* **Security Relevance:** A sudden surge in `404` status codes indicates automated directory brute-forcing, while `500` errors may indicate application crashes from fuzzing.
* **Job Market Context:** SOC Analysts configure SIEM alert rules to trigger when a single IP address generates more than fifty `401/403` status codes within two minutes.

#### 5. What did you observe when you ran your local Python web server?
* **Detailed Explanation:** Executing `python -m http.server 8000 --bind 127.0.0.1` initialized a single-threaded Python HTTP daemon bound strictly to the loopback address on TCP port 8000. Navigating to `http://127.0.0.1:8000/` in Chrome triggered real-time access logs in the PowerShell terminal, recording incoming `GET / HTTP/1.1 200 -` and `GET /style.css HTTP/1.1 200 -` requests along with automatic `404` logs for missing assets like `/favicon.ico`.
* **Security Relevance:** Demonstrates empirical client-server log generation directly from the server's operational perspective.

---

### SECTION D: PYTHON FUNDAMENTALS

#### 1. What is a variable?
* **Detailed Explanation:** A variable is a named symbolic reference bound to a specific location in computer memory that stores a data value, allowing it to be retrieved, modified, and reused throughout a program's execution lifecycle.
* **Real-World Example:** `failed_login_attempts = 5` stores the integer value `5` in memory under the name `failed_login_attempts`.
* **Security Relevance:** Managing variable scope and mutability prevents state corruption and data leaks in security scripts.

#### 2. What is a string?
* **Detailed Explanation:** A string (`str`) is an immutable data structure representing an ordered sequence of Unicode characters enclosed within single (`'`), double (`"`), or triple (`"""`) quotes.
* **Real-World Example:** `ip_address = "192.168.1.100"`.
* **Security Relevance:** Log parsing consists almost entirely of string operations (slicing, splitting, matching, regex extraction, and decoding).

#### 3. What is a function?
* **Detailed Explanation:** A function is a named, modular, reusable block of code that accepts input parameters, executes a specific sequence of instructions, and optionally returns an output value to the caller using the `return` statement.
* **Real-World Example:**
  ```python
  def calculate_risk(score):
      return score * 1.5
  
## 1. Self-Assessment Knowledge Check Matrix
| Topic Domain | Core Question | Confidence Status |
| :--- | :--- | :--- |
| **Computer Fundamentals** | Hardware vs. Software | **Green** (Confident) |
| **Computer Fundamentals** | Operating System Role | **Green** (Confident) |
| **Computer Fundamentals** | RAM vs. Storage | **Green** (Confident) |
| **Computer Fundamentals** | What is a Process? | **Green** (Confident) |
| **Networking** | IP Addresses & Addressing | **Green** (Confident) |
| **Networking** | DNS Resolution Mechanics | **Green** (Confident) |
| **Networking** | TCP vs. UDP Protocols | **Green** (Confident) |
| **Networking** | Port Identification | **Green** (Confident) |
| **Networking** | HTTPS & TLS Protection | **Green** (Confident) |
| **Web Fundamentals** | HTTP Request Structure | **Green** (Confident) |
| **Web Fundamentals** | HTTP Response Structure | **Green** (Confident) |
| **Web Fundamentals** | HTML vs. CSS Purpose | **Green** (Confident) |
| **Web Fundamentals** | Status Codes (`200`, `404`) | **Green** (Confident) |
| **Web Fundamentals** | Local Python Server Logs | **Green** (Confident) |
| **Python Foundations** | Variables & Data Types | **Green** (Confident) |
| **Python Foundations** | Functions & Modularity | **Green** (Confident) |
| **Python Foundations** | Exception Handling | **Green** (Confident) |

## 2. Topics to Revisit & Refine
* *Minor focus on advanced dictionary data manipulation and looping techniques in Python, which will be practiced during today's security log analyzer project.*

## 3. Three Questions to Resolve Today
1. How do we open, read, and parse structured text files line-by-line in Python?
2. How do we use `try-except` blocks to safely handle missing files or malformed log lines?
3. How can we build an automated script to count specific security events (like failed logins) from a dataset?
