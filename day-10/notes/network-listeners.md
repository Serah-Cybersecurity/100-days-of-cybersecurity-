# Day 10 - Listening Network Ports & Socket Inspection Notes

## 1. Core Concepts & Definitions
* **Listening Port:** A communication endpoint where a background service waits actively for incoming network connections.
* **Binding Interfaces:** 
  * **Loopback (`127.0.0.1`):** Accessible only locally from within the host.
  * **Wildcard (`0.0.0.0`):** Exposed across available network interfaces, requiring strict firewall oversight.

## 2. Practical Triage Commands Executed
* **Listening TCP Sockets Audit:**
  * **Command:** `ss -lnt`
  * **Flags Breakdown:** 
    * `-l`: Filters exclusively for listening sockets.
    * `-n`: Displays numeric addresses and port numbers (disabling reverse DNS lookups for speed and security).
    * `-t`: Restricts scope to Transmission Control Protocol sockets.
  * **Observation:** Successfully queried socket tables. An empty or minimal listener list under an unprivileged user session is entirely normal and expected.
* **Process Attribution Attempt:**
  * **Command:** `ss -lntp`
  * **Observation:** Attempted to map open ports to owning PIDs, noting that unprivileged user permissions restrict visibility into root-owned system daemons (a standard operational security constraint).

## 3. Defensive Security & Threat Hunting Insights
* **Role Consistency:** An analyst evaluates whether open listeners match the machine's intended purpose. Unfamiliar listeners warrant investigation rather than an automatic assumption of compromise.
* **Data Sanitization Rule:** Never publish raw socket inventories, internal IP bindings, or sensitive network ranges to public GitHub repositories.
