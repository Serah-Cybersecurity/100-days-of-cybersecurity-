# Technical Note: Cross-Tool Correlation Using Community ID

**Author:** Serah Mulwa

**Module:** Day 20 - Integrated Network Threat Hunting & Detection Engineering

## 1. Executive Summary

In a multi-tool security monitoring architecture, correlating alerts from an Intrusion Detection System (Suricata) with connection logs from a Network Security Monitor (Zeek) has historically been challenging. Each tool generates its own internal session trackers (`flow_id` in Suricata versus `uid` in Zeek), preventing direct comparison.

This technical note documents **Community ID**—an open standard flow-hashing specification that solves this correlation problem. By generating a standardized, hash-based identifier from network 5-tuples and a shared seed, Community ID allows analysts to seamlessly pivot between Suricata security alerts and Zeek connection records.

## 2. The Multi-Tool Correlation Challenge

When analyzing network traffic, disparate monitoring engines observe the exact same packet flows but assign independent identifiers:

* **Suricata EVE JSON Record:**
  ```json
  {
    "event_type": "alert",
    "src_ip": "192.0.2.10",
    "src_port": 53000,
    "dest_ip": "203.0.113.53",
    "dest_port": 53,
    "proto": "UDP",
    "flow_id": 123456789,
    "alert": { "signature": "LOCAL LAB DNS query for example.com" }
  }
  ```

* **Zeek Connection Record (`conn.log`):**
  ```json
  {
    "uid": "CExample123",
    "id.orig_h": "192.0.2.10",
    "id.orig_p": 53000,
    "id.resp_h": "203.0.113.53",
    "id.resp_p": 53,
    "proto": "udp"
  }
  ```

Because Suricata's `flow_id` (`123456789`) and Zeek's `uid` (`CExample123`) are generated independently, direct programmatic comparison is impossible without a shared reference point.

## 3. What is Community ID?

Developed as an open standard by Corelight, **Community ID** is a canonical hashing algorithm that normalizes network flow metadata into a uniform string representation (e.g., `1:L26St...`).

```
                  SAME NETWORK FLOW
                          │
        ┌─────────────────┴─────────────────┐
        ▼                                   ▼
    SURICATA                              ZEEK
        │                                   │
        ▼                                   ▼
    EVE RECORD                         CONN RECORD
        │                                   │
        └─────────────────┬─────────────────┘
                          ▼
                     COMMUNITY ID
                          │
                          ▼
                     SHARED VALUE
                          │
                          ▼
                   CROSS-TOOL PIVOT
```

### The Hashing Components:
The Community ID algorithm computes a cryptographic SHA-1 hash over:
1. Source IP Address
2. Destination IP Address
3. Source Port
4. Destination Port
5. Transport Protocol (`TCP`, `UDP`, `ICMP`)
6. A configurable numerical **Seed** (standardized as `0` across tools)

## 4. Operational Value in the SOC

* **Rapid Pivoting:** Analysts can execute a single query (`community_id == "1:..."`) to pull both the intrusion detection alert and the complete session metadata.
* **Reduced Complexity:** Eliminates the need for cumbersome multi-field matching logic (comparing source IPs, destination IPs, ports, and protocols across separate log files).
* **Automated Normalization:** Enables Python scripts and SIEM engines to stitch multi-vendor logs into a unified timeline effortlessly.

## 5. Technical Caveats & Limitations

1. **Seed Consistency:** Both Suricata and Zeek must be configured with the exact same seed value (e.g., `seed: 0`), or the resulting hashes will not match.
2. **Not a Unique Event ID:** Community ID identifies a *flow tuple*, not a unique timestamped event. Repeated connections reusing the same ports will share the same Community ID. **Always validate matches using timestamps.**
3. **NAT and Proxy Interference:** If network address translation (NAT) or load balancers alter IP tuples between monitoring points, Community ID correlation will fail unless translation logs are accounted for.

## 6. Key Portfolio Takeaways

* Community ID bridges the gap between signature alerting (Suricata) and stateful metadata logging (Zeek).
* Standardized flow hashing transforms disparate log formats into a relational cross-tool pivot mechanism.
* Professional analysts always combine Community ID matching with timestamp validation to ensure investigative accuracy.
