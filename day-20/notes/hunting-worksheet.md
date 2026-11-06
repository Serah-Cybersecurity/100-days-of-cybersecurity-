# Day 20 Threat-Hunting Worksheet

---

## Hunt 1: Cross-Tool DNS Correlation

* **Hypothesis:** When Suricata fires a signature alert for a DNS query matching `example.com`, Zeek independently records the underlying connection and protocol transactions under the identical Community ID flow hash.
* **Required Data Sources:** Suricata `eve.json`, Zeek `conn.log`, Zeek `dns.log`.

### Suricata Evidence:
* **Alert Signature:** `[1000001] LOCAL LAB DNS query for example.com`
* **Flow Tuple:** `10.0.2.15:42294 -> 192.168.100.1:53 (UDP)`
* **Extracted Community ID:** `1:qQZURsTvB7+LXx5x83z0/KkPQA=`

### Zeek Evidence:
* **Connection UID:** `CMNhdPSs13bACnDRh`
* **Community ID Hash:** `1:qQZURsTvB7+LXx5x83z0/KkPQA=`
* **DNS Log Query:** `example.com` (Type AAAA)

### Correlation Result:
* **Status:** **CONFIRMED (100% Match)**
* Both tools successfully recorded the exact flow, proving cross-sensor hash alignment and complete network flow visibility.

---

## Hunt 2: DNS Response Failure Analysis

* **Hypothesis:** Investigating non-successful DNS return codes (`rcode != 0`) reveals network endpoints encountering domain resolution errors or potential DGA (Domain Generation Algorithm) activity.
* **Required Data Sources:** Zeek `dns.log` (`query`, `rcode`, `rcode_name`, `id.orig_h`).

### Extracted Failure Telemetry (`jq` Query Results):
* **Observed Queries with Failures:** `jq -c 'select(.rcode != 0) | {ts, uid, query, rcode_name, source: ."id.orig_h"}' output/zeek/dns.log`
* **Findings:** Evaluated DNS response codes across `day20.pcap`. Records showed queries returning standard successful `NOERROR` (`rcode: 0`) responses for Debian NTP and target lab domain queries.

### Analyst Interpretation:
No suspicious high-frequency DNS failure spikes or DGA-like random domain failures were identified. Unsuccessful DNS responses must always be correlated with process line execution on the endpoint before declaring an incident.

---

## Hunt 3: Encrypted TLS Metadata Inspection

* **Hypothesis:** Transports utilizing TLS encryption conceal payload contents but reveal target server identity (SNI) and cryptographic negotiation strength in raw handshake metadata.
* **Required Data Sources:** Zeek `ssl.log` (`server_name`, `version`, `cipher`, `id.orig_h`, `id.resp_h`).

### Extracted TLS Handshake Telemetry:
* **Zeek UID:** `CgYkrq2WuUHKEgQkSj`
* **Target Server Name (SNI):** `104.20.23.154` / External endpoint
* **TLS Version:** TLSv1.3 (`TLS13`)
* **Cipher Suite:** `TLS_AES_256_GCM_SHA384`

### Visibility Limitations & Conclusion:
While Zeek `ssl.log` confirms the target server domain/IP and validates that strong modern encryption (TLS 1.3 with AES-256-GCM) was negotiated, **packet content payloads and HTTP GET/POST parameters remain fully encrypted**. To inspect payload contents, organizations must deploy endpoint detection and response (EDR) agents or inline SSL/TLS decryption proxies.
