# Network Security Monitoring Investigation Report

## 1. Investigation Details

* **Investigation ID:** INV-20261104-DNS-01
* **Date:** November 4, 2026
* **Analyst:** Serah Mulwa
* **Environment:** Parrot OS (Linux Kernel 6.x)
* **Data Source:** `pcap/dns-example.pcap`
* **Tools:** `tcpdump`, `Wireshark 4.x`, `Suricata 7.0.10`, `jq`, `Python 3.x`

---

## 2. Objective

The objective of this investigation is to demonstrate an offline Network Security Monitoring (NSM) workflow. This includes capturing live DNS traffic, performing forensic packet inspection, writing a custom local intrusion detection rule, replaying the captured traffic offline against Suricata, and analyzing generated EVE JSON telemetry both manually (via `jq`) and programmatically (via Python).

---

## 3. Environment

* **Operating System:** Parrot Security OS
* **Suricata Version:** 7.0.10 RELEASE (Running in System/User mode)
* **Capture Method:** CLI via `tcpdump`
* **Analysis Mode:** Offline PCAP Replay (`-r`)
* **Detection Rule ID:** `1000001` (Revision 1)

---

## 4. Evidence Collection

Packet capture traffic was recorded during an isolated network testing session:

* **Capture Interface:** Local Virtual Adapter (`eth0` / `wlan0`)
* **Capture Filter:** `udp port 53`
* **Capture File:** `pcap/dns-example.pcap`
* **Protocol Observed:** Domain Name System (DNS over UDP)
* **Total Packets Captured:** 8 packets (4 outbound DNS queries, 4 inbound DNS responses)

---

## 5. Detection Logic

To intercept queries directed at `example.com`, the following signature was written to `rules/local.rules`:

```text
alert dns any any -> any any (msg:"LOCAL LAB DNS query for example.com"; dns.query; content:"example.com"; nocase; sid:1000001; rev:1;)
```

### Component Breakdown:
* **`alert`**: Engine action to record the event without blocking offline traffic.
* **`dns`**: Application-layer protocol parser keyword.
* **`any any -> any any`**: Source and destination IP/Port pair matching.
* **`msg:"..."`**: Descriptive alert string printed to log outputs.
* **`dns.query;`**: Sticky buffer constraining string search strictly to requested domain fields.
* **`content:"example.com";`**: Target string pattern matched inside the buffer.
* **`nocase;`**: Case-insensitive evaluation.
* **`sid:1000001;`**: Unique local Signature Identifier.
* **`rev:1;`**: Initial revision index.

---

## 6. Results

* **Configuration Test (`suricata -T`):** Passed successfully (`Configuration provided was successfully loaded. Exiting.`).
* **PCAP Offline Processing (`suricata -r`):** Suricata successfully processed 1 file containing 8 packets (936 bytes).
* **Rule Matching:** The detection engine matched all 4 outbound DNS queries containing `example.com`.
* **Telemetry Output:** Generated structured records inside `output/suricata/eve.json` and `output/suricata/fast.log`.
* **Alert Information:** EVE JSON alerts contained exact timestamps, `src_ip` (`10.0.2.15`), `dest_ip` (`192.168.100.1`), query record types (`A` and `AAAA`), and `signature_id` (`1000001`).

---

## 7. Analysis

### Observed Facts
* Exactly 8 DNS packets were present in the capture file.
* Queries were generated for `example.com` targeting resolver `192.168.100.1`.
* Suricata generated 4 `alert` event types and 4 corresponding `dns` protocol event types in `eve.json`.
* Python script (`src/eve_summary.py`) processed 17 total log records without encountering malformed JSON lines.

### Interpretation
* The custom Suricata detection signature worked as designed, confirming that application-layer sticky buffers (`dns.query`) correctly match domain strings during offline packet dissection.

### Unknowns
* Host process identity (PID) originating the DNS requests cannot be determined from network packets alone without endpoint telemetry (EDR/Sysmon).

---

## 8. Detection Limitations

* **Scope:** The rule only matches string occurrences of `example.com` in plain-text DNS over UDP/53.
* **Evasion:** Encrypted DNS protocols (DoH - DNS over HTTPS, DoT - DNS over TLS) bypass this signature entirely.
* **False Positives:** Legitimate business communications to `example.com` trigger alerts under this basic rule.

---

## 9. Conclusion

The lab successfully verified the NSM pipeline. Suricata accurately parsed offline PCAPs, executed custom detection rules, and exported machine-readable EVE JSON telemetry that was parsed cleanly via command-line tools and Python scripts.

---

## 10. Recommendations

1. **Deploy Encrypted Protocol Inspection:** Implement TLS proxying or host-level EDR logging to monitor DNS queries utilizing DNS over HTTPS (DoH).
2. **Rule Tuning:** Combine network detection rules with reputation feeds to restrict alerts to known malicious domains rather than broad apex domains.
