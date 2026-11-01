# First Wireshark Capture

## Objective
To capture, filter, and analyze local network traffic using Wireshark to understand protocol encapsulation and packet headers.

## Environment
- **Operating System:** Parrot OS 7.3 KDE Security Edition / Windows Host[cite: 11]
- **Interface Used:** enp0s3 (Primary Ethernet NIC)[cite: 10]

## Authorization
Performed strictly on a personal, isolated virtual machine environment under direct ownership.

## Capture Method
Initiated a live capture session in Wireshark (`wireshark_enp0s3664CX3.pcapng`), generated local test traffic via terminal commands (`ping -c 3 127.0.0.1`), and captured live network DNS queries[cite: 10].

## Protocols Observed
- Ethernet II
- IPv4 / IPv6
- UDP / TCP
- DNS (Domain Name System)
- TLSv1.3

## Observations
- Directly observed UDP port 53 DNS queries and responses between local IP `10.0.2.15` and gateway `192.168.100.1`[cite: 10].
- Verified endpoint socket states using `ss -tuln`, observing active UDP listening services (such as port 123/NTP)[cite: 11].

## Interpretation
Traffic matched expected baseline behavior for standard system name resolution and local routing. No anomalous beaconing or unauthorized scanning detected.

## Limitations
Encrypted TLS payloads prevented inspection of application-layer text content, restricting analysis to handshake metadata, timing, and IP/port headers.

## Lessons Learned
Gained operational fluency in navigating Wireshark's three-pane view, capturing via `enp0s3`, and applying lowercase display filters (`dns`) to isolate specific protocol behavior[cite: 10].

## Next Steps
Correlating these packet capture timestamps and destination IPs with endpoint process execution and socket logs (`ss -tuln`) to map network traffic back to active local services[cite: 10, 11].
