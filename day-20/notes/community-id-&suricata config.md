# Technical Note: Cross-Tool Correlation Using Community ID & Suricata Configuration

**Author:** Serah Mulwa

**Module:** Day 20 - Integrated Network Threat Hunting & Detection Engineering

## 1. Executive Summary

In a multi-tool security monitoring architecture, correlating alerts from an Intrusion Detection System (Suricata) with connection logs from a Network Security Monitor (Zeek) has historically been challenging. Each tool generates its own internal session trackers (`flow_id` in Suricata versus `uid` in Zeek), preventing direct comparison.

This technical note documents **Community ID**—an open standard flow-hashing specification that solves this correlation problem—along with the hands-on configuration steps required to enable Community ID hashing within Suricata and validate signature loading using custom rules.

## 2. The Multi-Tool Correlation Challenge

When analyzing network traffic, disparate monitoring engines observe the exact same packet flows but assign independent identifiers:

* **Suricata EVE JSON Record:**

  ```json
  {
    "event_type": "alert",
    "src_ip": "10.0.2.15",
    "src_port": 48359,
    "dest_ip": "192.168.100.1",
    "dest_port": 53,
    "proto": "UDP",
    "flow_id": 432436730083357,
    "alert": { "signature": "LOCAL LAB DNS query for example.com" }
  }
  ```

* **Zeek Connection Record (`conn.log`):**

  ```json
  {
    "uid": "CExample123",
    "id.orig_h": "10.0.2.15",
    "id.orig_p": 48359,
    "id.resp_h": "192.168.100.1",
    "id.resp_p": 53,
    "proto": "udp"
  }
  ```

Because Suricata's `flow_id` and Zeek's `uid` are generated independently, direct programmatic comparison is impossible without a shared reference point.

## 3. What is Community ID?

Developed as an open standard by Corelight, **Community ID** is a canonical hashing algorithm that normalizes network flow metadata into a uniform string representation (e.g., `1:HxMkRMSXRcDEXn0KQrmp0iwucCw=`).

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
             1:HxMkRMSXRcDEXn0KQrmp0iwucCw=
                          │
                          ▼
                   CROSS-TOOL PIVOT
```

### The Hashing Components:

The Community ID algorithm computes a cryptographic SHA-1 hash over:

1. Source IP Address (`10.0.2.15`)
2. Destination IP Address (`192.168.100.1`)
3. Source Port (`48359`)
4. Destination Port (`53`)
5. Transport Protocol (`UDP`)
6. A configurable numerical **Seed** (standardized as `0` across tools)

## 4. Suricata Configuration Parameters (`suricata-day20.yaml`)

By default, Suricata does **not** enable Community ID flow hashing out of the box. To enable Community ID generation in EVE JSON output records for Day 20, the local configuration file `config/suricata-day20.yaml` was modified within the `- eve-log:` block:

```yaml
  # EVE @detailed log format / output setting
  - eve-log:
      enabled: yes
      filetype: regular
      filename: eve.json
      # Community ID support
      # Enables adding a community id header to the eve.json records.
      community-id: true
      community-id-seed: 0
```

### Critical Configuration Rules:
* `community-id: true`: Forces Suricata to compute and attach a `community_id` key to every JSON event object.
* `community-id-seed: 0`: Establishes seed `0` to match Zeek's standard hashing seed, ensuring identical hashes across tools.

## 5. Custom Signature Rule Syntax (`rules/local.rules`)

To test the integration pipeline and force an alert containing a Community ID hash, a benign custom Suricata rule was written to `rules/local.rules`:

```suricata
alert dns any any -> any any (msg:"LOCAL LAB DNS query for example.com"; dns.query; content:"example.com"; nocase; sid:1000001; rev:1;)
```

### Rule Structure Breakdown:
* `alert dns`: Triggers an alert when DNS payload traffic matches.
* `any any -> any any`: Inspects traffic from any source IP/port to any destination IP/port.
* `msg:"LOCAL LAB DNS query for example.com"`: Human-readable alert description written to log outputs.
* `dns.query; content:"example.com"; nocase;`: Inspects the DNS domain query string for `example.com` regardless of letter casing.
* `sid:1000001`: Unique local signature identification number.
* `rev:1`: Initial rule revision number.

## 6. Terminal Syntax Validation Output (`suricata -T`)

Before executing detection against test packet captures, Suricata's built-in engine tester was executed to validate YAML syntax and signature loading:

```bash
suricata -T -c ~/cybersecurity-journey/day-20/config/suricata-day20.yaml -S ~/cybersecurity-journey/day-20/rules/local.rules
```

### Verified Terminal Output:

```text
i: suricata: This is Suricata version 7.0.10 RELEASE running in SYSTEM mode
i: suricata: Configuration provided was successfully loaded. Exiting.
```

* **Validation Result:** Suricata parsed `suricata-day20.yaml` without syntax errors, loaded custom rule `sid:1000001`, and verified engine readiness.

## 7. Operational Value in the SOC

* **Rapid Pivoting:** Analysts can execute a single query (`community_id == "1:HxMkRMSXRcDEXn0KQrmp0iwucCw="`) to pull both the intrusion detection alert and the complete session metadata.
* **Reduced Complexity:** Eliminates the need for cumbersome multi-field matching logic across separate log files.
* **Automated Normalization:** Enables Python scripts and SIEM engines to stitch multi-vendor logs into a unified timeline effortlessly.

## 8. Key Portfolio Takeaways

* Community ID bridges the gap between signature alerting (Suricata) and stateful metadata logging (Zeek).
* Setting `community-id: true` and `community-id-seed: 0` in `suricata.yaml` is required for multi-sensor hash alignment.
* Validating configuration files with `suricata -T` prevents deployment errors and ensures rule loading in production SOC pipelines.
