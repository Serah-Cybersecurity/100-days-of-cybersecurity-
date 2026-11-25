# Technical Note: Live Packet Capture & Controlled Traffic Generation

**Author:** Serah Mulwa

**Module:** Day 19 - Network Threat Hunting with Zeek

## 1. Executive Summary

In network security monitoring, reliable telemetry relies entirely on the quality of underlying packet capture files (`.pcap`). Before running Zeek analysis or threat-hunting queries, analysts must know how to collect raw network packets securely and precisely from live interfaces.

This technical note documents our hands-on packet capture lab conducted on Parrot OS. It covers active network interface identification, `tcpdump` execution with Berkeley Packet Filters (BPFs), controlled traffic generation using `dig` and `curl`, and file validation via `capinfos`.

## 2. Identifying Active Network Interfaces

Before launching a capture, an analyst must determine which network interface card (NIC) is active and connected to the network.

### Commands Executed:
```
ip -br addr
ip route show default

```

### Observations:
* **`lo` (Loopback):** `UNKNOWN` status (`127.0.0.1`), used for internal host communication.
* **`enp0s3` (Ethernet Bridge):** `UP` status with IP `10.0.2.15/24`, serving as our active default gateway interface (`default via 10.0.2.2 dev enp0s3`).
* **`docker0`:** `DOWN` status (`172.17.0.1`), associated with local Docker bridge networking.

## 3. Executing `tcpdump` with Targeted BPF Filters

To prevent capturing excessive background network noise (such as local broadcast traffic or unrelated background services), we restricted our packet capture to DNS (UDP/TCP port 53) and HTTPS (TCP port 443).

### Command Executed:
```
sudo tcpdump -i enp0s3 -nn -s 0 -w pcap/day19.pcap '(udp port 53 or tcp port 53 or tcp port 443)'

```

### Option Breakdown:
* **`-i enp0s3`:** Directs `tcpdump` to listen exclusively on our active bridge interface.
* **`-nn`:** Disables reverse DNS lookups on IP addresses and ports, displaying raw numbers to improve performance and clarity.
* **`-s 0`:** Sets snapshot length to unlimited, ensuring complete packet payloads are captured without truncation.
* **`-w pcap/day19.pcap`:** Writes the raw binary capture directly into our project's `pcap/` folder.
* **BPF Filter `'(udp port 53 or ...)'`:** Filters traffic to capture only DNS and TLS/HTTPS sessions.

## 4. Generating Controlled Baseline Traffic

While `tcpdump` ran in our first terminal window, we opened a second terminal tab to generate clean, predictable test traffic:

1. **DNS Lookups (`dig`):**
   ```
   dig +tries=1 +time=2 example.com A
   dig +tries=1 +time=2 example.com AAAA
   ```
   * *Purpose:* Generates standard IPv4 (`A`) and IPv6 (`AAAA`) DNS resolution queries (`dns.log` telemetry).

2. **HTTPS Request (`curl`):**
   ```
   curl -I --max-time 10 https://example.com
   ```
   * *Purpose:* Sends an HTTP HEAD request over an encrypted TLS connection to port 443 (`ssl.log` telemetry), receiving a successful `HTTP/2 200 OK` response from Cloudflare.

## 5. Stopping and Validating the Capture

After generating traffic, we stopped `tcpdump` using `CTRL + C` (capturing 43 packets) and inspected the resulting file:

```
ls -lh pcap/
capinfos pcap/day19.pcap

```

### Key Capture Metadata:
* **File Name:** `day19.pcap`
* **File Size:** `11 KB`
* **Total Packets:** `43 packets`
* **Capture Duration:** `16.60 seconds`
* **Cryptographic Hashes:** Validated via SHA256 and SHA1 for forensic integrity.

## 6. Key Takeaways

* **Targeted BPF filters reduce noise:** Filtering by port and protocol ensures capture files remain lightweight and focused on relevant security telemetry.

* **`-nn` and `-s 0` are mandatory best practices:** Disabling name resolution speeds up triage, while zero snaplength guarantees full payload preservation.

* **Controlled testing validates tooling:** Generating known DNS and HTTPS traffic provides a reliable baseline for testing Zeek parser outputs.
