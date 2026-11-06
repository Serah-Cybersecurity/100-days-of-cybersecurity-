# Technical Note: Cross-Tool Correlation & Offline PCAP Analysis

**Author:** Serah Mulwa

**Module:** Day 20 - Integrated Network Threat Hunting & Detection Engineering

## 1. Executive Summary

In a multi-tool security monitoring architecture, correlating alerts from an Intrusion Detection System (Suricata) with connection logs from a Network Security Monitor (Zeek) has historically been challenging. Each tool generates its own internal session trackers (`flow_id` in Suricata versus `uid` in Zeek), preventing direct comparison.

This technical note documents **Community ID**—an open standard flow-hashing specification—and details the offline execution of both engines against a single packet capture file (`pcap/day20.pcap`) to achieve 100% hash correlation parity.

## 2. Multi-Tool Offline PCAP Execution Syntax

To evaluate network telemetry on the exact same packet sequence, Suricata and Zeek were executed against `pcap/day20.pcap` from the project root (`~/cybersecurity-journey/day-20`).

### 2.1 Suricata Execution Command

```bash
suricata \
  -c config/suricata-day20.yaml \
  -S rules/local.rules \
  -r pcap/day20.pcap \
  -l output/suricata
```

* `-c`: Loads the custom YAML configuration with `community-id: true` and `community-id-seed: 0`.
* `-S`: Loads custom local detection rule `sid:1000001` (`example.com` DNS query).
* `-r`: Reads offline packets from `pcap/day20.pcap`.
* `-l`: Directs EVE JSON output records to `output/suricata/eve.json`.

### 2.2 Zeek Execution Command

```bash
mkdir -p output/zeek
cd output/zeek
zeek -C \
  -r ../../pcap/day20.pcap \
  LogAscii::use_json=T \
  ../../scripts/community_id.zeek
cd ~/cybersecurity-journey/day-20
```

* `-C`: Ignores checksum errors resulting from hardware offloading.
* `-r`: Reads the identical target trace file `pcap/day20.pcap`.
* `LogAscii::use_json=T`: Forces Zeek to output structured JSON formatted logs instead of default tab-separated files.
* `../../scripts/community_id.zeek`: Loads custom policy specifying `@load policy/protocols/conn/community-id-logging` and `redef CommunityID::seed = 0;`.

---

## 3. Extracting Community ID Hashes via `jq`

With both tools generating structured JSON log files (`eve.json` and `conn.log`), command-line queries were executed using `jq` to isolate triggered alerts and verify flow hash generation.

### 3.1 Extracting Suricata Alert Community IDs

Querying Suricata `eve.json` for triggered alert events:

```bash
jq -c 'select(.event_type == "alert")' output/suricata/eve.json
```

Extracting the raw Community ID values:

```bash
jq -r 'select(.event_type == "alert") | .community_id // "NO COMMUNITY ID"' output/suricata/eve.json
```

**Verified Suricata Output Hashes:**
* `1:qQZURsTvB7+LXx5x83z0/KkPQA=`
* `1:P2oNim+dAcDZgQht0+q2HlbuHXU=`
* `1:I6puVD0/FGCszdfYg++4Rm1dA84=`

### 3.2 Extracting Zeek Connection Log Community IDs

Querying Zeek `conn.log` for 5-tuples and Community ID fields:

```bash
jq -c '{uid, community_id, source: ."id.orig_h", destination: ."id.resp_h", protocol: .proto}' output/zeek/conn.log
```

**Verified Zeek Output Record:**
```json
{"uid":"CMNhdPSs13bACnDRh","community_id":"1:qQZURsTvB7+LXx5x83z0/KkPQA=","source":"10.0.2.15","destination":"192.168.100.1","protocol":"udp"}
```

---

## 4. Cross-Tool Correlation Parity Proof

By comparing the outputs of Suricata's `eve.json` and Zeek's `conn.log`, exact hash parity was confirmed across both monitoring platforms:

| Attribute | Suricata EVE Alert | Zeek Connection Record | Match Status |
| :--- | :--- | :--- | :--- |
| **Source Endpoint** | `10.0.2.15` | `10.0.2.15` | **MATCH** |
| **Destination Endpoint** | `192.168.100.1:53` | `192.168.100.1:53` | **MATCH** |
| **Transport Protocol** | `UDP` | `udp` | **MATCH** |
| **Community ID Hash** | `1:qQZURsTvB7+LXx5x83z0/KkPQA=` | `1:qQZURsTvB7+LXx5x83z0/KkPQA=` | **PERFECT MATCH** |

---

## 5. Analyst Core Principles & Takeaways

### 1. Working Directory Context Matters
Always verify your current working directory using `pwd` before executing commands with relative paths (e.g., `../../pcap/day20.pcap`). Executing scripts from the wrong directory context leads to missing file errors during tool initialization.

### 2. JSON Consistency Streamlines Analysis
Passing `LogAscii::use_json=T` to Zeek normalizes its log format to align with Suricata's native EVE JSON. Ensuring both tools emit structured JSON allows unified log processing using `jq`, Elastic, or custom Python automation pipelines.

---

## 6. Portfolio Evidence Mapping

* `suricata-offline-pcap-execution.png`: Proves command-line execution of Suricata against `day20.pcap`.
* `zeek-conn-log-community-id-output.png`: Demonstrates Zeek JSON logging and `conn.log` hash generation.
* `suricata-eve-json-jq-alerts.png`: Validates `jq` queries returning matching Community ID flow strings.
