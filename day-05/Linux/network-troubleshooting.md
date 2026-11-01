# Linux Network Diagnostics and Troubleshooting

## Objective
To execute and document system-level Linux networking tools (`ip addr`, `ip route`, `ping`, `getent`) to verify network interface status, routing configurations, ICMP reachability, and OS name resolution paths.

## Diagnostics Record

### 1. Interface Configuration (`ip addr`)
- **Command:** `ip addr`[cite: 12]
- **Primary Interface:** `enp0s3`[cite: 12]
- **MAC Address:** `08:00:27:3b:a4:b2`[cite: 12]
- **Assigned IPv4 Address:** `10.0.2.15/24`[cite: 12]
- **Operational State:** `UP`[cite: 12]
- **Meaning:** The virtual interface is active and successfully leased a Layer 3 IP address from the VirtualBox DHCP scope.

### 2. Routing Table Analysis (`ip route`)
- **Command:** `ip route`[cite: 12]
- **Default Gateway:** `10.0.2.2` via `enp0s3`[cite: 12]
- **Local Subnet Route:** `10.0.2.0/24`[cite: 12]
- **Meaning:** Outbound packets destined for external subnets are directed to the virtual NAT gateway at `10.0.2.2`.

### 3. ICMP Reachability Tests (`ping`)
- **Loopback Test:** `ping -c 4 127.0.0.1`[cite: 12]
  - **Result:** 0% packet loss, RTT ~0.037ms[cite: 12].
  - **Meaning:** The internal Linux kernel TCP/IP network stack is healthy.
- **External IP Test:** `ping -c 4 172.66.147.243`[cite: 12]
  - **Result:** 0% packet loss, resolved IP `172.66.147.243`, RTT ~11.8ms[cite: 12].
  - **Meaning:** Gateway routing and external ICMP echo responses are functional.
  - **Caveat:** ICMP failure does not prove a web service is down, as firewalls often filter ICMP while keeping HTTP/HTTPS ports open.

### 4. Name Service Lookup (`getent ahosts`)
- **Command:** `getent ahosts example.com`[cite: 11]
- **Output:** Resolved IPv4 (`172.66.147.243`) and IPv6 addresses across STREAM (TCP) and DGRAM (UDP) socket types[cite: 11].
- **Meaning:** Verified the exact resolution logic utilized by system-level C libraries (`glibc`) including local host overrides.

## Errors & Troubleshooting Notes
- **Observation:** Initial attempt to capture packets via Wireshark resulted in `socket: Operation not permitted`.
- **Diagnosis:** Non-root user lacked direct raw packet socket access capabilities on device `enp0s3`.
- **Resolution:** Executed `sudo wireshark` to elevate administrative permissions for packet sniffing.
