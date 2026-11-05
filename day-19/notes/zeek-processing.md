# Technical Note: Offline PCAP Processing & JSON Parsing with Zeek 9.0.1

**Author:** Serah Mulwa   
**Module:** Day 19 - Network Threat Hunting with Zeek  

---

## 1. Executive Summary

While live Network Security Monitoring (NSM) sensors continuously stream telemetry into enterprise Security Information and Event Management (SIEM) systems, forensic investigators and threat hunters frequently need to analyze archived packet captures (`.pcap`) offline. 

This technical note documents the execution of **Zeek LTS 9.0.1** against a custom network capture file (`day19.pcap`). It details command-line execution flags, Docker volume mounting containerized workflows, and advanced command-line parsing of line-delimited JSON logs using `jq`.

---

## 2. Command Mechanics & Flag Breakdown

To process the offline capture file while avoiding false-positive errors caused by virtual network adapter artifacts, we executed Zeek using specific operational parameters:

```bash
zeek -C -r ../../pcap/day19.pcap LogAscii::use_json=T
```

### Parameter Breakdown:

| Component | Technical Function & Forensic Rationale |
| :--- | :--- |
| **`zeek`** | Invokes the core Zeek network analysis engine. |
| **`-C`** | **Disable Checksum Validation:** Ignores invalid IP/TCP/UDP checksums. Virtualized NICs often utilize "checksum offloading" where the host CPU offloads calculation to the physical hardware, causing packet captures to record incomplete checksums. Ignoring them prevents Zeek from silently dropping valid packets. |
| **`-r <filepath>`** | **Read Offline PCAP:** Instructs Zeek to process a pre-recorded capture file rather than listening live on an active interface. |
| **`LogAscii::use_json=T`** | **Structured JSON Output:** Formats all generated log records as line-delimited JSON rather than standard tab-separated values (TSV), simplifying automated ingestion and `jq` command-line triage. |

---

## 3. Containerized Processing Workflow (Docker)

To ensure environment portability and maintain clean execution isolation, we also verified processing via the official Zeek Docker image:

```bash
sudo docker run --rm \
  --entrypoint /bin/sh \
  -v "$PWD/pcap:/pcap:ro" \
  -v "$PWD/output/zeek:/logs" \
  -w /logs \
  zeek/zeek:9.0.1 \
  -c 'zeek -C -r /pcap/day19.pcap LogAscii::use_json=T'
```

### Key Engineering Practices Implemented:
* **Read-Only Volume Mount (`/pcap:ro`):** Preserves forensic integrity by mounting the raw evidence capture as read-only.
* **Ephemeral Container Cleanup (`--rm`):** Automatically destroys the container instance upon completion, leaving only generated log artifacts in `./output/zeek`.

---

## 4. Analysis of Generated Telemetry Logs

After processing `day19.pcap`, Zeek automatically dissected the protocol streams and generated the following specialized log files in `output/zeek/`:

* **`conn.log`:** Comprehensive 5-tuple connection state metadata.
* **`dns.log`:** Domain query and resolution records generated during test traffic execution (`example.com`).
* **`ssl.log`:** TLS handshake parameters, certificate metadata, and Server Name Indication (SNI) details.
* **`packet_filter.log`:** Log detailing the BPF filter rules active during analysis.

---

## 5. Advanced Telemetry Parsing with `jq`

Because logs were written in JSON format (`LogAscii::use_json=T`), we utilized `jq` to extract key incident investigation metrics cleanly without complex text-parsing scripts.

### Custom SOC Analyst Connection Summary Query:

```bash
jq -c '
{
  timestamp: .ts,
  uid: .uid,
  originator_ip: ."id.orig_h",
  responder_ip: ."id.resp_h",
  protocol: .proto,
  service: .service,
  duration: .duration,
  connection_state: .conn_state
}' output/zeek/conn.log
```

### Sample Parsed Output:

```json
{"timestamp":1793879608.917106,"uid":"C1ylQ419432UMYnqn2","originator_ip":"10.0.2.15","responder_ip":"192.168.100.1","protocol":"udp","service":"dns","duration":0.045783,"connection_state":"SF"}
{"timestamp":1793879624.770516,"uid":"CJ9ZcTl0c6Uw4h2W5","originator_ip":"10.0.2.15","responder_ip":"172.66.147.243","protocol":"tcp","service":"ssl","duration":0.749130,"connection_state":"SF"}
```

---

## 6. Key Takeaways

* **Disable checksums judiciously:** Use `-C` during virtualized lab analysis or PCAP testing to avoid dropping offloaded packets, but evaluate its security implications in production environments.
* **JSON output empowers SOC automation:** Outputting logs as JSON accelerates command-line parsing with `jq` and integrates seamlessly with modern enterprise SIEM pipelines.
* **Pivoting relies on structured metadata:** Extracted fields such as `uid`, `id.orig_h`, and `id.resp_h` form the foundational building blocks for multi-log event correlation.