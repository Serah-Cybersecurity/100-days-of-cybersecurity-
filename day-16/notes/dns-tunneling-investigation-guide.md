# DNS Tunneling Investigation & Wireshark Forensic Guide

## 1. Executive Overview & Objective

When investigating potential Data Exfiltration or Command-and-Control (C2) activity over port 53, standard log reviews are often insufficient. Security Operations Center (SOC) analysts must dive directly into packet captures (PCAPs) using Wireshark to inspect packet structures, query lengths, and response anomalies.

This guide provides a step-by-step walkthrough for investigating suspected **DNS Tunneling** (MITRE ATT&CK **T1071.004**) using Wireshark and TShark.

---

## 2. Preparation & Environment Setup

Before opening your packet capture, ensure your investigative environment meets professional standards:
* **Evidence Integrity:** Never modify the original `.pcap` or `.pcapng` file. Always work on a forensic copy and calculate its SHA-256 hash first.
* **Time Normalization:** Ensure your Wireshark time display format is set to UTC (`View` -> `Time Display Format` -> `UTC Date and Time of Day`) to align with Windows or Linux system event logs.

---

## 3. Step-by-Step Wireshark Investigation Workflow

### Step 1: Open the Packet Capture and Review Protocol Hierarchy
1. Open Wireshark and load your suspect capture file.
2. Navigate to **Statistics** -> **Protocol Hierarchy**.
3. **What to look for:** Check the percentage of UDP traffic. If DNS (`dns`) constitutes an abnormally large share of total packet volume or bandwidth compared to normal browsing traffic, flag it for deeper review.

### Step 2: Apply High-Level DNS Display Filters
Instead of looking at raw packets, isolate standard DNS traffic by typing the following in the display filter bar:
```wireshark
dns
```
To narrow your view specifically to queries sent by clients, filter by query records:
```wireshark
dns.flags.response == 0
```

### Step 3: Hunt for Long Query Names (Subdomain Smuggling)
DNS tunneling tools (such as `dnscat2` or `iodine`) pack encoded data into long subdomain labels. Filter for queries where the name length exceeds standard thresholds:
```wireshark
dns.qry.name.len > 50
```
* **Analysis:** Expand the packet in the Packet Details pane, expand **Domain Name System (query)** -> **Queries**, and examine the queried FQDN. Look for high character entropy (random-looking strings of Base64 or Hex characters).

### Step 4: Isolate TXT Record Exfiltration
Attackers frequently use `TXT` records because they allow larger data payloads in responses. Filter for `TXT` type queries (`type 16`):
```wireshark
dns.qry.type == 16
```
* **Analysis:** Check the Answer section of the response packets to see if arbitrary binary or text strings are being passed back and forth.

### Step 5: Check for High `NXDOMAIN` RCODE Spikes
If malware is using a Domain Generation Algorithm (DGA) or guessing subdomains, it will trigger numerous name errors. Filter for response code 3 (`NXDOMAIN`):
```wireshark
dns.flags.rcode == 3
```
* **Analysis:** Group by source IP or destination domain to see if a single internal workstation is generating thousands of non-existent domain requests.

---

## 4. Key Indicators of Compromise (IoCs) to Document

When compiling your investigation report, document these specific forensic artifacts:
1. **Source Endpoint IP & MAC:** The infected internal host initiating the traffic.
2. **Suspicious Domain / Base FQDN:** The external domain receiving the tunneled queries.
3. **Query Length & Entropy:** Average length of subdomains and frequency of requests.
4. **Record Types Utilized:** Heavy reliance on `TXT`, `NULL`, or custom record types.
5. **Volume Metrics:** Total packet count, bytes transferred, and duration of the session.

---

## 5. MITRE ATT&CK Mapping

* **Tactics:** Command and Control, Exfiltration
* **Technique:** `T1071.004` — Application Layer Protocol: DNS
* **Detection Strategy Reference:** MITRE DET0400 (Behavioral Detection of DNS Tunnelling and Application Layer Abuse)
