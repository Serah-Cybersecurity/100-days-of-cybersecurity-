# Day 16 - DNS Security, Threat Detection, and MITRE ATT&CK Alignment

## 1. Why Attackers Love to Abuse DNS

When you first learn about networking, DNS feels like a simple, helpful utility that translates website names into IP addresses. But when you look at it through the lens of a security analyst, DNS takes on a completely different meaning.

Because almost every corporate network relies on DNS for everyday business, firewalls and perimeter controls are almost always configured to permit outbound DNS traffic (UDP/TCP port 53). Attackers know this and routinely exploit it. If an attacker can't open a direct web or SSH shell because strict firewalls block standard ports, they will often smuggle their traffic right through port 53.

## 2. DNS-Based Command-and-Control (C2)

### 2.1 What Is C2?
Command-and-control (C2) is the communication lifeline between an adversary's remote server and a compromised machine inside a target network. Once malware infects a host, it needs a way to receive instructions (*"What file should I steal next?"*) and send back stolen data.

### 2.2 MITRE ATT&CK Mapping
In the MITRE ATT&CK framework, this is categorized under **T1071.004 — Application Layer Protocol: DNS**. Attackers use this technique to blend malicious command traffic into ordinary network activity, making it look like standard web browsing or administrative lookups to basic security tools.

## 3. DNS Tunneling: Smuggling Data Through Subdomains

DNS tunneling is a technique where attackers use DNS queries and responses as a secret carrier pigeon to move data or commands past firewalls. 

Here is how it typically works in the real world:
1. **Infection:** Malware runs on a workstation inside the corporate network.
2. **Data Encoding:** The malware takes a sensitive file or password database, encodes it into Base64 or Hex, and chops it into small chunks.
3. **Subdomain Smuggling:** It tacks those encoded chunks onto the front of a malicious domain controlled by the attacker (e.g., `aHR0cHM6Ly.malicious-domain.com`).
4. **Recursive Resolution:** The corporate endpoint sends this query to the local recursive resolver. The resolver forwards it out to the internet, pushing it straight through the firewall without raising alarms.
5. **Authoritative Capture:** The query eventually reaches the attacker's own **authoritative name server**. The attacker's server reads the encoded chunk, replies with the next command hidden inside a DNS response record, and completes a covert two-way communication channel.

## 4. Key Indicators of Compromise (IoCs) & Anomaly Detection

As a SOC analyst, your job isn't to block every unusual query blindly, but to investigate specific behavioral red flags. Here are the core indicators you should keep on your radar:

* **Unusually High Query Volume:** A single host flooding thousands of requests could indicate automated malware beaconing or active data exfiltration. *(False positive check: A busy web server or heavy API polling).*
* **Very Long Query Names:** Abnormally long strings in the subdomain section usually point to data packed into DNS labels during tunneling. *(False positive check: Complex CDN hashing paths or cloud storage URLs).*
* **Massive Volumes of Unique Subdomains:** Often a sign of a **Domain Generation Algorithm (DGA)**, where malware programmatically generates hundreds of random domain names per minute trying to find an active C2 server. *(False positive check: Dynamic DNS clients or multi-tenant cloud applications).*
* **High TXT Record Volume:** `TXT` records store raw text strings. Attackers love abusing them to pass executable payloads or config updates past defenses. *(False positive check: Legitimate email verification protocols like SPF, DKIM, and DMARC).*
* **High `NXDOMAIN` Frequency:** A flood of `NXDOMAIN` (Non-Existent Domain) responses from one host means it is querying domains that don't exist—often a sign of a DGA or misconfiguration. *(False positive check: Human typing typos in browsers).*
* **Unexpected Processes Making DNS Requests:** Seeing an unknown binary or a system tool like `notepad.exe` initiating external DNS lookups instead of an authorized browser.

## 5. MITRE's Detection Guidance (DET0400)

When security engineering teams build automated detection pipelines, they rely on formalized strategies like **MITRE Detection Strategy DET0400** (*Behavioral Detection of DNS Tunnelling and Application Layer Abuse*). 

This strategy focuses on spotting behavioral anomalies rather than relying on static blocklists, prompting analysts to monitor:
* Statistical spikes in subdomain character entropy and label lengths.
* Sudden deviations from baseline query frequency per endpoint.
* Processes generating network traffic that violate standard operational baselines.

## 6. What to Remember as an Analyst
Never jump to conclusions based on a single metric. Context is everything. Always compare what an endpoint is doing against its normal organizational baseline before declaring an incident!
