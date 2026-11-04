# Technical Note: Suricata Signature Anatomy & Detection Engineering

**Author:** Serah  Mulwa

**Date:** November 4, 2026

**Module:** Day 18 - Network Security Monitoring & Intrusion Detection

## 1. Executive Summary

In a modern Security Operations Center (SOC), detection engineering is the discipline of creating, testing, and refining detection signatures to identify malicious activity across network traffic. Suricata relies on a declarative rule syntax to inspect network frames, application payloads, and session flows in real time. 

This technical note breaks down the structure of Suricata rules, explores the core detection methodologies (signature-based, anomaly-based, and behavioral detection), details thresholding techniques used to eliminate false positives, and provides concrete examples of custom signatures designed for network security monitoring.

## 2. Detection Methodologies Comparison

Threat detection engines utilize three primary analytical approaches to identify unauthorized or suspicious network activity:

```
[ Incoming Network Packet ]
             │
             ├───> [ Signature-Based ] ───> Matches known static pattern/byte sequence?
             ├───> [ Anomaly-Based ]   ───> Deviates significantly from network baseline?
             └───> [ Behavioral ]      ───> Matches suspicious activity workflow sequence?
```

| Detection Method | Mechanics | Key Strengths | Operational Limitations |
| :--- | :--- | :--- | :--- |
| **Signature-Based** | Matches packets against static rules containing known strings, byte patterns, or header attributes. | High precision, low processing overhead, clear attribution for known threats. | Blind to zero-day exploits, encrypted payloads, and modified malware variants. |
| **Anomaly-Based** | Establishes a baseline of "normal" traffic and flags statistical deviations (e.g., sudden spikes in volume). | Can identify novel, unclassified threats and unusual exfiltration attempts. | High false-positive rate; legitimate IT operational changes can trigger false alarms. |
| **Behavioral** | Analyzes sequences of actions across protocols and time (e.g., DNS query followed by RDP connection). | Focuses on adversary Tactics, Techniques, and Procedures (TTPs) rather than static IOCs. | Requires sophisticated correlation engines and multi-source logging pipelines. |

## 3. Anatomy of a Suricata Signature

A Suricata rule consists of two main logical parts: the **Rule Header** (defining action, protocol, IP addresses, ports, and direction) and the **Rule Options** (enclosed in parentheses, defining match conditions, metadata, and unique identifiers).

```
  Rule Action        Source IP / Port          Dest IP / Port
 ┌──────────┐       ┌────────────────┐        ┌──────────────┐
   alert tcp $EXTERNAL_NET any -> $HOME_NET 3389 (msg:"ET SCAN Potential RDP Brute Force"; flow:to_server,established; threshold:type threshold, track by_src, count 5, seconds 60; classtype:attempted-recon; sid:1000001; rev:1;)
         └───┘                    └─┘            └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
       Protocol                Direction                                                                               Rule Options
```

### 3.1 The Rule Header

1. **Action:** Tells Suricata what operational action to take when traffic matches:
   * `alert`: Generates a log entry and notification without modifying packet traversal.
   * `pass`: Immediately stops rule evaluation for this packet and permits it through.
   * `drop`: (IPS Mode) Drops the packet instantly and writes an alert.
   * `reject`: (IPS Mode) Drops the packet and sends an active reset (TCP RST) or ICMP unreachable back to sender.

2. **Protocol:** Defines the Layer 4 or Layer 7 protocol to inspect: `tcp`, `udp`, `icmp`, `ip`, `http`, `dns`, `tls`, `smb`.

3. **Source / Destination IP Addresses:** Defines originating and targeting networks. Variables like `$HOME_NET` (internal assets) and `$EXTERNAL_NET` (outside entities) are defined in `/etc/suricata/suricata.yaml`.

4. **Ports:** Specific port numbers (e.g., `80`, `3389`), ranges (e.g., `1024:65535`), or `any`. Exclusions are indicated with `!` (e.g., `!80`).

5. **Direction Operator:**
   * `->`: Matches traffic flowing from source (left) to destination (right).
   * `<>`: Matches bi-directional traffic between both hosts.

### 3.2 Core Rule Options

Rule options are separated by semicolons and dictate payload evaluation parameters:

* **`msg:"..."`**: The human-readable string displayed in `fast.log` and `eve.json` when the alert triggers.
* **`flow:to_server,established`**: Ensures the rule only evaluates active, fully established TCP sessions moving toward the destination server, ignoring failed SYN attempts.
* **`content:"..."`**: Searches for a specific ASCII or hexadecimal string in the packet payload.
* **`nocase`**: Modifies `content` to perform case-insensitive matching.
* **`depth` / `offset`**: Restricts content searching to a specific byte range within the payload for performance optimization.
* **`classtype`**: Categories defined in `/etc/suricata/classification.config` (e.g., `attempted-admin`, `bad-unknown`, `trojan-activity`).
* **`sid` (Signature ID):** A unique numerical identifier for the rule:
  * `1` to `999,999`: Reserved for core rulesets (e.g., Emerging Threats, Snort rules).
  * `1,000,000+`: Reserved for local custom user rules.
* **`rev` (Revision):** Incremental version number for rule tracking.

## 4. Thresholding & Alert Suppression

In high-volume enterprise networks, aggressive signature matching without thresholding leads to **alert fatigue**—overwhelming SOC analysts with thousands of duplicate alerts for a single event stream.

### 4.1 Threshold Syntax

Suricata provides built-in thresholding to control alert generation rates:

```suricata
threshold:type <threshold|limit|both>, track <by_src|by_dst>, count <N>, seconds <S>
```

* **`threshold` Type:** Fires an alert every $N$ times the rule matches within an $S$-second window. Ideal for detecting brute-force or port-scan thresholds.
* **`limit` Type:** Fires a maximum of $N$ alerts within an $S$-second window, suppressing subsequent matches until the timer resets. Ideal for limiting repetitive noise.
* **`track by_src` / `track by_dst`**: Tracks occurrences independently per source IP address or destination IP address.

## 5. Practical Rule Examples & Field Scenarios

### Example 1: Custom DNS Tunneling Detection Rule
Targets suspicious DNS queries containing abnormally long or suspicious subdomains sent to external resolvers.

```suricata
alert dns $HOME_NET any -> $EXTERNAL_NET 53 (msg:"LOCAL DISCOVERY Suspicious Long DNS Query - Potential Tunneling"; dns.query; content:"."; pcre:"/^[a-zA-Z0-9]{30,}\./"; classtype:bad-unknown; sid:1000002; rev:1;)
```

### Example 2: Outbound SMB Exposure Detection Rule
Detects internal systems attempting to establish Server Message Block (SMB) file-sharing connections to external networks on TCP port 445 (often associated with ransomware exfiltration or worm propagation).

```suricata
alert tcp $HOME_NET any -> $EXTERNAL_NET 445 (msg:"POLICY OUTBOUND SMB Traffic Detected to External Network"; flow:to_server,established; classtype:policy-violation; sid:1000003; rev:1;)
```

## 6. False Positives vs. False Negatives

Detection engineers must balance precision and recall when deploying new rules:

```
                  ACTUAL STATE
              Malicious     Legitimate
            ┌─────────────┬─────────────┐
  ALERT     │    True     │    False    │
  FIRED     │  Positive   │  Positive   │
DETECTION   ├─────────────┼─────────────┤
  NO        │    False    │    True     │
  ALERT     │  Negative   │  Positive   │
            └─────────────┴─────────────┘
```

* **False Positive (FP):** The sensor alerts on legitimate traffic (e.g., an internal software update matching an overly broad malware signature). FPs drain analyst time and cause alert fatigue.
* **False Negative (FN):** Malicious activity passes through undetected because no signature exists or rule conditions were too narrow. FNs lead to unmonitored breaches.

## 7. Job Market Applications

* **Detection Engineering:** Security engineers write, tune, and test custom Suricata rules during active incident response to detect newly published IOCs (Indicators of Compromise).
* **Threat Hunting:** Analysts analyze `eve.json` telemetry outputs to identify custom protocol violations and refine alert thresholds for enterprise SIEM platforms.
