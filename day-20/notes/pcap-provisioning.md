# Technical Note: PCAP Provisioning & Multi-Protocol Telemetry Verification

**Author:** Serah Mulwa

**Module:** Day 20 - Integrated Network Threat Hunting & Detection Engineering

## 1. Executive Summary

A foundational rule of cross-tool network threat hunting is that all detection engines under evaluation must process the exact same packet capture (`.pcap`) file. Relying on separate capture files introduces timing variances, missing frames, and flow tuple discrepancies that corrupt Community ID hashes and undermine cross-tool correlation.

This technical note documents the methodology used to capture, verify, and inspect the baseline network traffic stored in `pcap/day20.pcap`. It details both command-line verification using `capinfos` and deep-packet visual analysis via Wireshark.

## 2. PCAP Provisioning Methodology

The baseline network traffic was captured live from the primary network interface (`enp0s3`) on the analyst's Parrot OS virtual machine using `tcpdump`.

### Capture Command:

```bash
sudo tcpdump -i enp0s3 -nn -s 0 -w ~/cybersecurity-journey/day-20/pcap/day20.pcap '(udp port 53 or tcp port 53 or tcp port 443)'
```

### Traffic Generation Steps:

To ensure representative protocols were available for multi-tool correlation, the following traffic streams were initiated during the active capture window:

1. **IPv4 DNS Lookup:** Executed `dig +tries=1 +time=2 example.com A` to test UDP port 53 name resolution.
2. **IPv6 DNS Lookup:** Executed `dig +tries=1 +time=2 example.com AAAA` to generate IPv6 query telemetry.
3. **Encrypted Web Traffic:** Executed `curl -I --max-time 10 https://example.com` to initiate a full TCP 3-way handshake and TLS 1.3 session over destination port 443.

## 3. Command-Line PCAP Verification

After terminating the capture, file integrity and statistical metrics were verified using `capinfos` and `tcpdump`:

### Metadata Breakdown (`capinfos` Output):

* **File Name:** `pcap/day20.pcap`
* **File Type:** Wireshark/tcpdump - pcap
* **Packet Count:** 60 packets
* **File Size:** 13 kB (12 kB data size)
* **Capture Duration:** 31.75 seconds
* **SHA256 Hash:** `b10820b281021bb5b5ead6901a4259ae97522a43329804f4f6653d412990795a`
* **SHA1 Hash:** `c68d60c14cca82eaf97cbf48b7e0a441f93e410b`

### CLI Packet Stream Inspection (`tcpdump -nn -r`):

Command-line inspection confirmed standard DNS queries issued from internal IP `10.0.2.15` to local gateway resolver `192.168.100.1#53`, returning A record IP addresses `172.66.147.243` and `104.20.23.154`.

## 4. Wireshark Protocol Inspection & Evidence

Visual packet inspection in Wireshark verified the presence of all three target protocols using specific display filters:

| Protocol Filter | Observed Telemetry & Frame Details | Verification Status |
| ----- | ----- | ----- |
| **`dns`** | Standard DNS queries (`A` and `AAAA` for `example.com`) and responses; 24 matching frames (40.0% of capture). | **CONFIRMED PRESENT** |
| **`tls`** | Encrypted HTTPS handshake containing `Client Hello` with Server Name Indication (SNI) set to `example.com`; 11 matching frames (18.3% of capture). | **CONFIRMED PRESENT** |
| **`tcp`** | Complete TCP 3-way handshakes (`SYN`, `SYN-ACK`, `ACK`) established on port 443 with Cloudflare edge IPs; 36 matching frames (60.0% of capture). | **CONFIRMED PRESENT** |

## 5. Portfolio Evidence & Screenshot Mapping

The following verified screenshot artifacts are preserved in `day-20/screenshots/` to validate this phase of the lab:

* `pcap-copy-and-capinfos.png`: Validates baseline PCAP metadata and file transfer integrity.
* `pcap-tcpdump-inspection.png`: Demonstrates CLI inspection of raw DNS and TCP frame headers.
* `traffic-dig-a-record.png`: Captures active execution of IPv4 DNS resolution for `example.com`.
* `traffic-dig-aaaa-and-curl.png`: Documents active generation of IPv6 queries and HTTP/2 200 header responses over TLS.
* `fresh-pcap-capture-capinfos.png`: Confirms live packet collection producing 60 packets with complete SHA256 hashes.
* `wireshark-dns-filter.png`: Displays Wireshark packet list filtered by `dns`.
* `wireshark-tls-filter.png`: Displays Wireshark packet list filtered by `tls`, showing SNI domain fields.
* `wireshark-tcp-filter.png`: Displays Wireshark packet list filtered by `tcp`, highlighting initial connection flags.

## 6. Key Takeaways

* Never assume a capture file contains necessary telemetry; always verify packet totals, duration, and protocols using `capinfos` and Wireshark.
* Grounding cross-tool analysis in a single, verified PCAP file ensures that downstream detection alerts in Suricata and session logs in Zeek map to the exact same 5-tuples.
* Preserving cryptographic file hashes (SHA256/SHA1) of test PCAPs establishes a clear chain of custody for forensic reporting.
