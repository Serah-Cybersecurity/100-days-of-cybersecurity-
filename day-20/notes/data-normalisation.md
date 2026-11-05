# Technical Note: Data Normalisation & Common Schemas in Enterprise Security

**Author:** Serah Mulwa

**Module:** Day 20 - Integrated Network Threat Hunting & Detection Engineering

## 1. Executive Summary

In a modern Security Operations Center (SOC), telemetry flows in from a multitude of independent security tools—intrusion detection systems (Suricata), network monitors (Zeek), firewalls, operating systems, and cloud environments. Each vendor formats their logs using proprietary naming conventions. Without data normalisation, security analysts are forced to learn dozens of distinct field schemas, severely slowing down incident investigation and SIEM querying.

This technical note documents the concept of data normalisation and introduces the **Elastic Common Schema (ECS)**. By mapping disparate tool outputs into a uniform schema, analysts and automation scripts can process multi-vendor security events seamlessly.

## 2. The Multi-Vendor Field Discrepancy Problem

Consider how different security platforms represent standard network 5-tuple attributes:

| Conceptual Field | Suricata Field Name | Zeek Field Name | Firewall / Netflow Log |
| :--- | :--- | :--- | :--- |
| **Source IP** | `src_ip` | `id.orig_h` | `src_addr` |
| **Source Port** | `src_port` | `id.orig_p` | `src_port` |
| **Destination IP** | `dest_ip` | `id.resp_h` | `dst_addr` |
| **Destination Port** | `dest_port` | `id.resp_p` | `dst_port` |
| **Transport Protocol**| `proto` | `proto` | `protocol` |
| **Flow Identifier** | `community_id` | `community_id` | N/A |

If an analyst must write distinct query syntax for every single log source during an active investigation, triage becomes inefficient and prone to human error.

## 3. Introducing the Elastic Common Schema (ECS)

To eliminate field-naming chaos, enterprise SIEM platforms utilize standardized common schemas. The industry standard **Elastic Common Schema (ECS)** defines uniform field namespaces across all security events:

* `source.ip`: The IP address of the device originating the connection.
* `source.port`: The port number on the originating host.
* `destination.ip`: The IP address of the device receiving the connection.
* `destination.port`: The port number on the destination host.
* `network.transport`: The transport protocol (`tcp`, `udp`, `icmp`).
* `network.protocol`: The application-layer protocol (`dns`, `http`, `tls`).
* `network.community_id`: The standardized Community ID flow hash.

## 4. Why Normalisation Matters in the Job Market

* **SIEM Query Efficiency:** Writing detection queries against standard ECS fields (`source.ip: 10.0.2.15`) allows a single rule to search across Suricata, Zeek, and firewall logs simultaneously.
* **Automation Scalability:** Python scripts or SOAR playbooks become vastly simpler when they ingest raw vendor logs, normalise them into a common dictionary structure, and pass them to downstream correlation engines.

## 5. Key Portfolio Takeaways

* Raw logs from different security vendors speak entirely different dialects.
* Data normalisation translates multi-vendor logs into a single universal language.
* Mastering schema standards like ECS is an essential competency for any junior SOC analyst or SIEM engineer.
