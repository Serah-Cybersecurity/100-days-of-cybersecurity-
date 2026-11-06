# Technical Note: Network Event Data Normalisation & ECS Mapping

**Author:** Serah Mulwa  
**Module:** Day 20 - Integrated Network Threat Hunting & Detection Engineering  

---

## 1. Executive Summary

In enterprise Security Operations Centers (SOCs), network security monitoring reliance on multi-vendor telemetry often creates log friction due to non-standardized field names. Suricata outputs fields like `src_ip`, `dest_port`, and `proto` in its EVE JSON log stream, whereas Zeek identifies the exact same attributes as `id.orig_h`, `id.resp_p`, and `proto` in its connection logs. 

To conduct efficient multi-vendor threat hunting, build reusable automated scripts, and construct centralized SIEM dashboards, raw event streams must be normalized into a standardized taxonomy. This technical note documents the educational subset mapping derived from the **Elastic Common Schema (ECS)** used during Day 20.

---

## 2. Field Mapping Table (Educational ECS Subset)

The following matrix maps raw vendor log keys from Suricata and Zeek to a single standardized common schema:

| Common Field Schema | Suricata EVE Source Field | Zeek Connection (`conn.log`) Field | Purpose & Description |
| :--- | :--- | :--- | :--- |
| `@timestamp` | `timestamp` | `ts` | ISO-8601 or epoch timestamp of event occurrence. |
| `source.ip` | `src_ip` | `id.orig_h` | Originating host IP address. |
| `source.port` | `src_port` | `id.orig_p` | Source ephemeral or service port. |
| `destination.ip` | `dest_ip` | `id.resp_h` | Destination target host IP address. |
| `destination.port` | `dest_port` | `id.resp_p` | Destination target service port. |
| `network.transport` | `proto` | `proto` | Transport-layer protocol (`tcp`, `udp`, `icmp`). |
| `network.community_id` | `community_id` | `community_id` | Standardized 5-tuple flow hash string. |
| `event.dataset` | Suricata event type | Zeek log name | Identifies log module (e.g., `suricata.alert`, `zeek.dns`). |
| `event.kind` | Alert classification | Network event classification | Standardized category (`alert`, `event`, `metric`). |

---

## 3. The Purpose of Separating Raw Logs from Normalised Schemas

1. **Decoupling Log Sources from Detection Logic:** Writing SIEM detection rules against vendor-neutral field names (`source.ip`) ensures that rules remain functional even if underlying log engines are changed or upgraded.
2. **Elimination of Conditional Scripting:** Automated triage scripts can iterate through unified JSON dictionaries without needing custom `if/else` checks for every distinct vendor tool.
3. **Optimized Multi-Tool Searching:** SOC analysts can execute single-query searches across historical datasets without needing to remember tool-specific key conventions.

---

## 4. Key Portfolio Takeaways & Core Analyst Principles

1. **Normalisation is Structural:** Transforming log formats into a common schema does not alter or modify the underlying evidence payload—it simply provides a consistent, predictable lens through which to query and analyze raw telemetry.
2. **ECS Compliance Accelerates Response:** Adopting industry-standard schemas like ECS minimizes operational friction, streamlines log ingestion pipelines, and speeds up triage during high-stress incident investigations.
