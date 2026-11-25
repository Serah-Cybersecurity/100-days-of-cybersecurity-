# Technical Note: Offline PCAP Analysis & EVE JSON Telemetry Parsing

**Author:** Serah Mulwa

**Module:** Day 18 - Network Security Monitoring & Intrusion Detection

## 1. Executive Summary

In enterprise environments, security analysts rarely inspect raw network packets in real-time for historical investigations. Instead, sensors record packet captures (`.pcap`) and feed them into detection engines like Suricata for offline analysis. 

This technical note documents our hands-on execution of offline packet replay (`-r`), the generation of structured Extensible Event Format (EVE) JSON logs (`eve.json`), and the use of command-line tools like `jq` to parse and extract specific security alerts.

---

## 2. Running Suricata in Offline Mode

When operating on pre-captured traffic, we bypass live interface listening and instruct Suricata to process saved packet captures. We created a dedicated output directory and executed our offline analysis command:

```bash
# Create dedicated output directory
mkdir -p output/suricata

# Run Suricata offline against our DNS PCAP using our custom rule
sudo suricata -c /etc/suricata/suricata.yaml -S rules/local.rules -r pcap/dns-example.pcap -l output/suricata
```

### Explanation of Core Flags:
* **`-r pcap/dns-example.pcap`:** Tells Suricata to read recorded packets from our file rather than sniffing a live network interface.
* **`-S rules/local.rules`:** Forces the engine to load *only* our custom rule, isolating the test environment.
* **`-l output/suricata`:** Directs all generated telemetry logs into our designated subfolder.

Checking the contents of our output directory (`ls -lah output/suricata`) confirmed the creation of essential log files:
* **`eve.json`:** The master structured JSON event log containing all network telemetry.
* **`fast.log`:** A lightweight, human-readable text log of alerts.
* **`stats.log`:** Engine performance and packet processing metrics.

---

## 3. Parsing EVE JSON Telemetry with `jq`

Modern Security Information and Event Management (SIEM) platforms ingest Suricata's `eve.json` logs because JSON is universally structured and easy for machines to index. To inspect these logs directly from the Linux terminal, we use `jq` (a lightweight command-line JSON processor).

### 1. Extracting Alert Events
To filter `eve.json` and isolate only events where our custom rule triggered an alert, we ran:
```bash
jq -c 'select(.event_type == "alert")' output/suricata/eve.json
```
* **Observed Result:** Our custom rule (`sid:1000001`, `LOCAL LAB DNS query for example.com`) successfully matched our DNS packets, outputting clean JSON alert structures.

### 2. Inspecting Raw DNS Protocol Events
To view protocol-specific metadata parsed from the network stream:
```bash
jq -c 'select(.event_type == "dns")' output/suricata/eve.json | head
```

### 3. Creating a Custom SOC Analyst View
To strip away unnecessary JSON fields and present only the critical forensic data (Timestamp, Source IP, Destination IP, and Alert Message), we executed a formatted query:
```bash
jq -c 'select(.event_type == "alert") | {timestamp, src_ip, dest_ip, alert: .alert.signature}' output/suricata/eve.json
```

---

## 4. Systematic Troubleshooting Methodology

During our lab execution, we encountered a couple of configuration hurdles (such as rule duplication and directory permission warnings). When debugging Suricata, always follow a structured troubleshooting process rather than guessing:

1. **Verify Input PCAP:** Ensure the packet capture actually holds the expected traffic using `tcpdump -nn -r pcap/dns-example.pcap`.
2. **Inspect Rules:** Check for duplicate signatures or syntax errors using `cat rules/local.rules`.
3. **Test Syntax:** Always validate rule and configuration files before running analysis using `suricata -T`.
4. **Confirm Outputs:** Verify that EVE logging is enabled in `/etc/suricata/suricata.yaml`.

---

## 5. Job Market Relevance

* **SOC Analyst & Incident Responder:** In real-world investigations, analysts ingest suspect PCAPs into sandbox environments running Suricata. Mastering offline replay (`-r`) allows them to quickly test newly published threat intel signatures against historical captures.
* **SIEM / Detection Engineer:** Writing efficient `jq` queries and log parsing rules is a daily requirement for engineering teams building automated alerting pipelines in enterprise SOCs.
