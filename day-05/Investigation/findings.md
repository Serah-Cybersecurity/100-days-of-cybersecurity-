# Network Investigation Findings

## 1. Objective
To systematically analyze network telemetry logs to summarize traffic patterns, isolate malformed records, and evaluate potential security risks objectively.

## 2. Scope
- **Included:** 10 log records containing timestamps, source/destination IPs, destination ports, and protocols.
- **Excluded:** Live PCAP packet captures, endpoint process execution lists (Sysmon/EDR), and user authentication logs.

## 3. Data Source
`sample_events.json` (Synthetic training dataset).

## 4. Method
Executed `network_event_analyzer.py` to parse JSON records, apply input schema validation, segregate malformed entries, and aggregate protocol and port counters.

## 5. Direct Observations
- **Total Ingested:** 10 records.
- **Valid Records:** 7 records processed.
- **Malformed/Rejected Records:** 3 records (due to out-of-range port numbers, missing fields, or invalid data types).
- **Protocols Observed:** 5 TCP events, 2 UDP events.
- **Destination Ports Observed:** Port 443 (3 events), Port 53 (2 events), Port 80 (1 event), Port 22 (1 event).

## 6. Interpretation
- **Port 443:** Conventionally associated with HTTPS traffic, but port numbers alone do not guarantee encrypted web protocols.
- **Port 53:** Conventionally associated with DNS domain name lookups.
- **Port 22:** Conventionally associated with SSH remote administration.
- **Port 80:** Conventionally associated with unencrypted HTTP web traffic.

## 7. Alternative Explanations
1. **Benign User Activity:** A user browsing standard web services while an administrator performs routine remote maintenance.
2. **Automated Scripts:** A background update application or scanning tool querying external endpoints.

## 8. Limitations
- Header-only log analysis cannot verify payload contents or actual application behavior.
- Small sample size (10 events) cannot establish baseline host network patterns.
- No process name or user ID attached to network sockets.

## 9. Questions Requiring Further Investigation
1. Which local executable binary initiated the connection on port 22?
2. What specific domain names were queried via port 53?
3. What do endpoint EDR logs show at timestamps `09:00:00Z` through `09:00:09Z`?

## 10. Conclusion
The dataset establishes that 7 valid connections occurred across standard ports. However, the available evidence is **INSUFFICIENT** to establish whether the activity is malicious or benign.
