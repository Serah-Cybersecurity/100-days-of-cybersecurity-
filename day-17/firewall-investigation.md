# Firewall Event Investigation

## 1. Investigation Overview

- **Investigation ID:** INV-2026-1103-01
- **Date:** 2026-11-03
- **Analyst:** Serah Kathini (Women Techsters Fellow)
- **Data source:** Synthetic firewall event log (`sample_firewall_events.csv`)
- **Environment:** Lab / Portfolio Triage Environment
- **Scope:** Initial automated parsing, frequency counting, and behavioral pattern identification

## 2. Objective

To analyze synthetic firewall event logs using an automated Python triage script (`firewall_triage.py`), identify unauthorized or blocked connection attempts, evaluate traffic distributions, and provide defensive recommendations without overstepping evidentiary boundaries.

## 3. Dataset Description

- **Dataset type:** Structured CSV firewall log export
- **Number of records:** 10 events analyzed
- **Fields available:** timestamp, src_ip, src_port, dst_ip, dst_port, protocol, direction, action, interface, state
- **Time range:** 2026-11-03T09:00:01Z to 2026-11-03T09:06:00Z
- **Known limitations:** Synthetic data records; lacks rule IDs, full NAT translation mappings, and endpoint process telemetry.

## 4. Observations

### Observation 1: Repeated Denied Connection Pattern
Automated log parsing identified 5 total `DENY`/`DROP` actions out of 10 events. A specific external source IP (`203.0.113.50`) generated 3 consecutive inbound connection attempts targeting destination port `3389` over `TCP` within a 9-second window (09:01:20 to 09:01:29 UTC).

### Observation 2: Action Distribution
The dataset reflects an even split between allowed outbound traffic and blocked inbound attempts:
- **ALLOW:** 5 records (primarily outbound HTTPS/DNS and established inbound sessions).
- **DENY:** 5 records (inbound probes targeting internal services).

### Observation 3: Secondary Anomalies
A single outbound connection attempt from internal host `192.0.2.10` to external host `198.51.100.25` on port `445` (Microsoft-DS / SMB) was blocked (`DENY`), indicating local firewall policy enforcement against outbound SMB traffic.

## 5. Technical Analysis (Primary Incident Pattern)

- **Source IP:** `203.0.113.50` (External entity)
- **Destination IP:** `192.0.2.10` (Internal target host)
- **Source Ports:** `49811`, `49812`, `49813` (Ephemeral client ports)
- **Destination Port:** `3389` (Remote Desktop Protocol - RDP)
- **Protocol:** `TCP`
- **Direction:** `INBOUND`
- **Firewall Action:** `DENY`
- **Connection State:** `NEW`

*Explanation of Fields:* The connection state `NEW` combined with destination port `3389` indicates an external host attempting to initiate a new Remote Desktop session, which was successfully intercepted and blocked by the firewall's inbound policy.

## 6. Assessment (Evidentiary Separation)

### Confirmed Facts
- The firewall recorded 3 inbound connection attempts from `203.0.113.50` to `192.0.2.10` on TCP port 3389.
- All three attempts were evaluated against firewall rules and assigned a `DENY` action.

### Reasonable Interpretations
- The rapid succession and repetition of three requests strongly suggest an automated scan or brute-force probe targeting Remote Desktop services.

### Unverified Hypotheses
- The data does **not** establish malicious intent, successful compromise, or human-driven attacker activity. The source IP could be a misconfigured legitimate scanner or automated botnet sweep.

## 7. Limitations

The conclusions drawn in this report are constrained by several missing telemetry vectors:
- **Missing Rule IDs:** Firewall logs did not specify which exact rule ID triggered the block.
- **Missing Endpoint Data:** No endpoint logs (Sysmon/Windows Event Logs) were available to verify if the target host was actively listening or suffering resource exhaustion.
- **Missing Identity:** User account context and geographical attribution were absent.

## 8. Recommendations

1. **Monitor Source IP:** Add source IP `203.0.113.50` to SIEM watchlist correlation rules.
2. **Review RDP Exposure:** Verify that RDP (Port 3389) is not exposed directly to the public internet; enforce VPN access or Zero Trust network boundaries.
3. **Log Retention:** Ensure production firewalls are configured to log dropped packets with maximum verbosity and rule ID mapping.

## 9. Conclusion

A repeated denied connection pattern was observed targeting TCP port 3389 from an external source IP. The firewall successfully recorded and denied these events. While the pattern merits review and baseline threat intelligence correlation in a live environment, the data does not establish whether a compromise occurred.
