# Structured SPL Search Records & Investigation Audit Log

**Author:** Serah Kathini Mulwa

**Program:** Women Techsters Fellowship — Cybersecurity Track

**Module:** Day 22 — Splunk Fundamentals & Search Processing Language (SPL)

**Target Index:** `cybersecurity_lab` (`sourcetype="_json"`, `source="normalised_events.jsonl"`, `host="parrot"`)

**Dataset:** `normalised_events.jsonl` (8 normalized Elastic Common Schema events timestamped `2026-11-06T08:00:00Z` – `2026-11-06T08:08:00Z`)

## 1. Why I Record Searches in a Structured Format

A raw list of SPL commands without context is hard to audit later. When I revisit a repository—or when a hiring manager or teammate reviews my investigation—seeing only a bare `stats` or `timechart` command leaves key questions unanswered: *What time range did I search? What exact numbers came back? How did I interpret them, and what did I avoid assuming?*

Using a consistent **8-part investigation record** (`Objective`, `SPL`, `Data Source`, `Time Range`, `Results`, `Interpretation`, `Limitations`, and `Next Investigation Step`) keeps every search transparent, reproducible, and tied directly to actual outputs from my Splunk screenshots.

## 2. Standard 8-Part Search Record Template

````markdown
## Search: [Investigation Title]

### Objective
[State the specific security, schema, or auditing question this search answers.]

### SPL
```spl
[Insert exact SPL query executed]
```

### Data Source
`cybersecurity_lab`

### Time Range
[Record the exact time picker setting or search window]

### Results
[Record the actual output observed in Splunk]

### Interpretation
[Explain what the observed results suggest as an investigative lead]

### Limitations
[Explain what cannot be concluded and any dataset or schema constraints]

### Next Investigation Step
[State what additional telemetry, correlation, or verification would be useful next]
````

---

## 3. Executed Search Records (`cybersecurity_lab`)

## Search: Ingestion Verification & Schema Inspection

### Objective
Verify that `normalised_events.jsonl` is indexed into `cybersecurity_lab` with `_json` source type extraction, inspect extracted fields and summary statistics, and audit event time (`_time`) against ingestion time (`_indextime`).

### SPL
```spl
index=cybersecurity_lab
| head 5
| fieldsummary
```

```spl
index=cybersecurity_lab
| eval index_time=_indextime, lag_seconds=_indextime - _time
| table _time index_time lag_seconds event.action
```

### Data Source
`cybersecurity_lab` (`normalised_events.jsonl`, `sourcetype="_json"`, `host="parrot"`)

### Time Range
`All time` (synthetic dataset events timestamped `2026-11-06T08:00:00Z` – `2026-11-06T08:08:00Z`, uploaded into Splunk on `2026-11-24`)

### Results
* **Full index scan (`index=cybersecurity_lab`):** Confirms `8` total events (`2026-11-06 08:00:00` through `2026-11-06 08:08:00` UTC).
* **Field summary (`| head 5 | fieldsummary`):** Summarizes `5` sampled events across `50` extracted fields (`@timestamp`, `date_hour`, `date_mday`, `date_minute`, `date_month`, nested JSON fields, and metadata).
* **Event vs. ingestion lag audit (`_indextime - _time`):** All `8` events share `index_time = 1795524011` (epoch timestamp from upload on `2026-11-24`), with `lag_seconds` spanning `1571531` to `1572011` seconds (~18.2 days between the synthetic `2026-11-06 08:00` event timestamps and the `2026-11-24` file upload).

### Interpretation
Confirming index contents, extracted fields, and `_indextime - _time` before hunting prevents misreading synthetic historical batch uploads as live real-time telemetry. The ~18.2-day difference between `_time` and `_indextime` is expected here because a static synthetic file from `2026-11-06` was uploaded on `2026-11-24`.

### Limitations
* **Historical Batch Upload:** Because `normalised_events.jsonl` was uploaded as a static file rather than streamed continuously by a live forwarder, `lag_seconds` reflects upload timing relative to synthetic event dates—not live network or agent pipeline latency.
* **Subset Sampling in `fieldsummary`:** Running `| head 5 | fieldsummary` inspects `5` events (`50` fields), so fields appearing only on the remaining `3` events require searching across all `8` events.

### Next Investigation Step
Inspect specific fields (`event.action`, `event.outcome`, `source.ip`, `destination.ip`, `user.name`) across all `8` events in `cybersecurity_lab` to build baseline distributions.

---

## Search: Event Action Breakdown & Authentication Outcomes

### Objective
Summarize all indexed events by `event.action` and evaluate authentication `failure` versus `success` outcomes across `cybersecurity_lab`.

### SPL
```spl
index=cybersecurity_lab
| stats count by event.action
| sort - count
```

```spl
index=cybersecurity_lab "event.category{}"="authentication"
| stats count by event.outcome
| sort - count
```

### Data Source
`cybersecurity_lab` (`normalised_events.jsonl`, `sourcetype="_json"`)

### Time Range
`All time` (synthetic dataset events timestamped `2026-11-06T08:00:00Z` – `2026-11-06T08:08:00Z`)

### Results
* **Event action breakdown (`stats count by event.action | sort - count` across all `8` events):**
  * `authentication_failure`: `2`
  * `authentication_success`: `2`
  * `intrusion_detection_alert`: `2`
  * `network_connection_allowed`: `1`
  * `network_connection_blocked`: `1`
* **Authentication outcomes:** `2` `failure` events and `2` `success` events (`4` authentication events total).

### Interpretation
Grouping directly by `event.action` cleanly surfaces every activity type present in the `8`-event lab dataset (`2` failed logins, `2` successful logins, `2` Suricata IDS alerts, `1` allowed connection, and `1` blocked connection). Earlier exploratory attempts filtering on unquoted `event.category="authentication"` returned `0` events because Splunk extracted array fields under `"event.category{}"`—a helpful reminder to verify extracted field names before relying on a filter.

### Limitations
* **Counts Are Leads, Not Proof:** Two authentication failures and two successes in a small synthetic sample do not prove credential compromise or malicious intent.
* **Schema Array Nuance:** Always verify how nested JSON arrays are extracted in Splunk (`"event.category{}"` vs. `event.action`) so valid events are not missed during filtering.

### Next Investigation Step
Pivot directly into `event.action="authentication_failure"` to examine which user account and originating `source.ip` generated the two failed logins.

---

## Search: Failed Authentication by Source

### Objective
Identify originating IP addresses (`source.ip`) associated with failed authentication events and measure failure counts.

### SPL
```spl
index=cybersecurity_lab sourcetype="_json" event.outcome="failure"
| stats count AS failed_attempts by source.ip
| sort - failed_attempts
```

*(Note: When `user.name` is present on failure events, pairing `count AS failed_attempts` with `dc(user.name) AS unique_accounts` also helps distinguish single-account retries from multi-account password spraying.)*

### Data Source
`cybersecurity_lab` (`normalised_events.jsonl`, `sourcetype="_json"`)

### Time Range
`All time` (synthetic dataset events timestamped `2026-11-06T08:00:00Z` – `2026-11-06T08:08:00Z`)

### Results
* **Query output (`2` events matched):**
  * `source.ip = 192.0.2.25`: `failed_attempts = 2` (and shown in the dashboard drill-down table as `alex` with `2` failures and `1` unique account).

### Interpretation
Documentation-range address `192.0.2.25` generated `2` failed authentication events against account `alex` during the lab window. Seeing two failures from one IP against a single account is a focused triage lead—it could be a user mistyping a password, a stale credential/token, or early brute-force probing.

### Limitations
* **No Proof of Compromise or Attack:** Two failed authentication events from a synthetic test IP do not prove account takeover, brute-force malice, or intrusion success.
* **NAT / Proxy Ambiguity:** In real enterprise networks, a single `source.ip` can represent a NAT gateway, VPN, or proxy shared by multiple users, while attackers can also rotate across multiple IPs.

### Next Investigation Step
Cross-reference `192.0.2.25` and `alex` against successful authentication events (`2026-11-06 08:05:00` and `08:06:00`) and network activity (`192.0.2.25` blocked connection at `08:02:00` and Suricata alert at `08:03:00`) to see how the timeline connects.

---

## Search: DNS & Network Telemetry Audit

### Objective
Audit DNS query telemetry (`dns.question.name`) and inspect network-category / intrusion detection telemetry in `cybersecurity_lab`.

### SPL
```spl
index=cybersecurity_lab
| stats count by dns.question.name
| sort - count
```

```spl
index=cybersecurity_lab event.action="intrusion_detection_alert"
| table _time host.name event.provider event.action event.outcome
```

### Data Source
`cybersecurity_lab` (`normalised_events.jsonl`, `sourcetype="_json"`)

### Time Range
`All time` (synthetic dataset events timestamped `2026-11-06T08:00:00Z` – `2026-11-06T08:08:00Z`)

### Results
* **DNS query field check (`dns.question.name`):** Returned `0` results because this 8-event `normalised_events.jsonl` sample does not contain DNS query payload records (`dns.question.name`).
* **Network & Suricata IDS telemetry:**
  * Two `intrusion_detection_alert` events occurred at `2026-11-06 08:03:00` and `2026-11-06 08:08:00` with `event.provider="suricata"`, `event.outcome="detected"`, and `host.name="null"`.
  * Network connection records in the dataset consist of `network_connection_blocked` (`192.0.2.25 -> 198.51.100.20` on port `443` at `08:02:00`) and `network_connection_allowed` (`192.0.2.50 -> 198.51.100.50` on port `80` at `08:07:00`).

### Interpretation
Documenting that `dns.question.name` returned `0` results accurately reflects a telemetry gap in this sample dataset rather than forcing fake DNS findings. Meanwhile, the two Suricata `intrusion_detection_alert` events (`detected`) alongside the blocked port `443` connection (`192.0.2.25 -> 198.51.100.20`) provide concrete network leads to inspect further.

### Limitations
* **Missing DNS Query Logs in Sample Data:** Because no DNS resolution fields are present in this 8-event sample, domain-level DNS hunting (such as suspicious domains or tunneling indicators) cannot be performed on this batch alone—and my dashboard's **DNS Activity** table summarizes available network actions (`intrusion_detection_alert`, `network_connection_allowed`, `network_connection_blocked`) instead.
* **IDS Alert != Confirmed Intrusion:** `event.outcome="detected"` means a Suricata rule matched traffic; without signature details, packet captures, or endpoint host logs (`host.name` is `null` here), it does not prove compromise.

### Next Investigation Step
Inspect the full JSON fields of both Suricata events and both firewall connection events, and add dedicated DNS query events (`dns.question.name`) in future dataset iterations to support domain-level analysis.

---

## Search: Temporal Event Volume & Time-Filtered Actions

### Objective
Analyze event cadence over explicit time buckets (`span=1h`) and inspect event actions across time-filtered windows.

### SPL
```spl
index=cybersecurity_lab
| timechart span=1h count
```

```spl
index=cybersecurity_lab
| timechart span=1h count by event.outcome
```

### Data Source
`cybersecurity_lab` (`normalised_events.jsonl`, `sourcetype="_json"`)

### Time Range
`All time` (synthetic dataset events timestamped `2026-11-06T08:00:00Z` – `2026-11-06T08:08:00Z`)

### Results
* **Hourly volume (`timechart span=1h count`):** All `8` events fall inside the single `2026-11-06 08:00` hourly bucket (`count = 8`).
* **Hourly outcome breakdown (`timechart span=1h count by event.outcome`):** Within `2026-11-06 08:00`, outcomes are `allowed = 1`, `denied = 1`, `detected = 2`, `failure = 2`, and `success = 2`.

### Interpretation
All eight events in the sample dataset cluster within the `08:00` hour (`08:00:00` to `08:08:00` UTC). Explicitly setting `span=1h` keeps time bucketing consistent and predictable across searches and dashboard panels.

### Limitations
* **One-Hour Granularity:** A `span=1h` bucket groups every event within that hour into one interval, smoothing out minute-by-minute sequencing inside the `08:00–08:08` window.
* **Timing Alone Does Not Explain Intent:** A timechart shows *when* events occurred, not *why*—raw events and context are still required for root-cause analysis.

### Next Investigation Step
Sort individual events chronologically by `_time` (`| table _time event.action event.outcome source.ip destination.ip destination.port user.name | sort _time`) to trace the exact order of events between `08:00:00` and `08:08:00`.