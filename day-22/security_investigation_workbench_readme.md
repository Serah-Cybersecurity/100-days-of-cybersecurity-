# Security Investigation Workbench with Splunk

**Author:** Serah Kathini Mulwa  
**Program:** Women Techsters Fellowship — Cybersecurity Track  
**Module:** Day 22 — Splunk Fundamentals & Search Processing Language (SPL)  
**Target Index:** `cybersecurity_lab` (`sourcetype="_json"`)  

---

## 1. Project Overview

In this project, I built a local SIEM analysis workflow using synthetic security telemetry generated and normalized through my previous Day 21 Mini-SIEM project. Rather than treating Splunk as a simple log viewer, I structured this repository as an end-to-end security investigation workbench designed to mirror real-world Security Operations Center (SOC) triage, field verification, and analytical reporting habits.

Specifically, I used Splunk Enterprise in an isolated local environment to:
- **Ingest security events** from a normalized JSON Lines (`normalised_events.jsonl`) telemetry file into a dedicated training index (`cybersecurity_lab`).
- **Explore fields** and validate how nested Elastic Common Schema (ECS) JSON objects and arrays are extracted at search time.
- **Analyse authentication activity** across user accounts, outcomes (`success` vs. `failure`), and originating IP addresses.
- **Examine network telemetry** covering perimeter firewall decisions (`allowed` vs. `blocked`), destination ports, and Suricata intrusion detection alerts.
- **Aggregate event counts** using statistical SPL transformations (`stats`, `dc()`, `sort`) to rank outliers and summarize behavior.
- **Investigate time-based patterns** using explicit temporal bucketing (`timechart span=1h`) to reconstruct event timelines.
- **Build a dashboard** (*Security Operations Overview — Training Environment*) organized into KPI, trend/comparison, and drill-down investigation bands.
- **Document investigation findings** rigorously, separating observed telemetry facts from analytical hypotheses and known limitations.

*Scope Note: All data used in this workbench consists strictly of synthetic, authorized lab telemetry analyzed inside a local training environment. This project demonstrates practical SIEM investigation and SPL skills and is not a formal Splunk vendor certification.*

---

## 2. Objectives

The primary engineering and analytical goals of this workbench are to:
1. **Isolate Lab Telemetry Safely:** Configure a dedicated non-default Splunk index (`cybersecurity_lab`) so training logs remain cleanly separated from Splunk internal logs (`_internal`, `main`).
2. **Validate Schema-on-the-Fly Parsing:** Inspect extracted fields before hunting so nested JSON structures and array fields (such as `"event.category{}"`) are queried accurately.
3. **Execute Structured SOC Hunts:** Run repeatable SPL queries covering authentication baselines, failed login attribution, network/IDS telemetry, firewall actions, and time-series cadence.
4. **Build Purpose-Driven Visualizations:** Design an operational dashboard where every panel answers a specific triage question and documents its own limitations.
5. **Practice Analytical Restraint:** Treat high failure counts, blocked connections, or IDS alerts as **investigative leads** rather than automatic proof of compromise.

---

## 3. Tools and Technologies

- **SIEM Platform:** Splunk Enterprise (Local Lab Instance, Splunk Web on port `8000`)
- **Query Language:** Search Processing Language (SPL) — `search`, `table`, `fields`, `sort`, `head`, `dedup`, `stats`, `eval`, `where`, `timechart`, `fieldsummary`
- **Telemetry Schema:** Elastic Common Schema (ECS)-aligned normalized JSON Lines (`normalised_events.jsonl`, `sourcetype="_json"`)
- **Upstream Pipeline:** Day 21 Python Mini-SIEM Log Normalization Pipeline
- **Documentation & Version Control:** Markdown, Git, GitHub

---

## 4. Architecture

The workflow follows a clear three-stage data pipeline from synthetic log normalization to interactive SOC investigation:

```text
[Day 21 Mini-SIEM Pipeline]
        │  Generates & normalizes synthetic security logs
        ▼
[normalised_events.jsonl]
        │  Uploaded via Splunk Web (sourcetype="_json")
        ▼
[Splunk Enterprise Index: cybersecurity_lab]
        │  Search-time JSON & array field extraction
        ├──────────────────────────────┬──────────────────────────────┐
        ▼                              ▼                              ▼
[Ad-Hoc SPL Hunts]      [SOC Overview Dashboard]       [Investigation Report]
(5 Core Modules)        (7 Operational Panels)         (Facts vs. Assumptions)
```

### Repository Layout

```text
day22-splunk-security-investigation/
├── README.md                          # Complete workbench overview & evidence guide
├── docs/
│   ├── splunk_ingestion_guide.md      # Step-by-step index setup & onboarding notes
│   ├── data_dictionary.md             # Normalized ECS field mappings & array quirks
│   ├── investigation_methodology.md   # 5-stage hunt workflow & detection thinking
│   ├── spl_fundamentals.md            # Detailed reference for 11 core SPL commands
│   └── limitations.md                 # Dataset constraints, time ranges & scale notes
├── queries/
│   └── 01_authentication_anomalies.spl # Reusable SPL hunt queries
├── dashboards/
│   └── dashboard_design.md            # Architecture & specs for all 7 dashboard panels
├── reports/
│   └── investigation_report.md        # Structured SOC findings, SPL logs & evidence index
└── screenshots/                       # Curated visual verification captures
```

---

## 5. Dataset Description

- **File Name:** `normalised_events.jsonl`
- **Format:** JSON Lines (one self-contained JSON event record per line)
- **Total Volume:** 8 discrete normalized security events
- **Event Timestamp Window:** `2026-11-06T08:00:00Z` through `2026-11-06T08:10:00Z`
- **Observer Breakdown:**
  - `observer.type="endpoint"`: 4 events (authentication activity)
  - `observer.type="network"`: 4 events (firewall connection logs and Suricata IDS alerts)
- **Event Action Distribution (`event.action`):**
  - `authentication_failure`: 2 events
  - `authentication_success`: 2 events
  - `intrusion_detection_alert` (`event.provider="suricata"`): 2 events
  - `network_connection_allowed`: 1 event
  - `network_connection_blocked`: 1 event

---

## 6. Data Ingestion

To maintain clean data hygiene and avoid polluting Splunk's default `main` index:
1. **Created Dedicated Index:** Navigated to **Settings > Indexes > New Index** and created `cybersecurity_lab` as an `Events` index.
2. **Uploaded Structured Telemetry:** Used **Settings > Add Data > Upload** to import `normalised_events.jsonl`.
3. **Verified Sourcetype & Timestamps:** Selected `sourcetype="_json"` and confirmed in the preview pane that Splunk parsed `@timestamp` (`2026-11-06 08:00:00.000 AM`) and nested JSON blocks accurately before submitting.
4. **Validated Searchability:** Executed `index=cybersecurity_lab | head 1` and `index=cybersecurity_lab | fieldsummary` under **All time** to verify all 8 events and extracted fields before running investigations.

*(Full onboarding steps are documented in `docs/splunk_ingestion_guide.md`.)*

---

## 7. SPL Searches

Every search in this repository follows two core SPL habits: **filter early, aggregate late** (scoping `index=cybersecurity_lab` and filtering attributes before `stats` or `timechart`) and **explicitly define `span`** on time-series charts.

### Authentication Baseline & Outcomes
```spl
index=cybersecurity_lab "event.category{}"="authentication"
| stats count by event.outcome
| sort - count
```

### Failed Authentication Attribution by Source
```spl
index=cybersecurity_lab "event.category{}"="authentication" event.outcome="failure"
| stats count AS failed_attempts, dc(user.name) AS unique_accounts, values(user.name) AS targeted_users by source.ip
| sort - failed_attempts
```

### Suricata Intrusion Detection Alerts
```spl
index=cybersecurity_lab event.action="intrusion_detection_alert"
| table _time host.name event.provider event.action event.outcome
```

### Perimeter Firewall Connection Audit
```spl
index=cybersecurity_lab event.action=*network*
| table _time source.ip destination.ip destination.port event.action
```

### Temporal Event Volume & Outcome Trends
```spl
index=cybersecurity_lab
| timechart span=1h count by event.outcome
```

---

## 8. Investigation Scenarios

I structured my analysis around five core SOC investigation scenarios, documented in full in `reports/investigation_report.md`:

1. **Scenario 1 — Authentication Activity Baseline:** Audited login success versus failure ratios across endpoint telemetry (`2` failures, `2` successes) to establish baseline account activity.
2. **Scenario 2 — Failed Authentication Source Attribution:** Grouped authentication failures by `source.ip` and measured target cardinality (`dc(user.name)`) to differentiate single-account retries from multi-account password spraying.
3. **Scenario 3 — DNS & Intrusion Detection Telemetry:** Audited `dns.question.name` (confirming 0 DNS query records in this sample batch) and pivoted to Suricata NIDS telemetry, isolating 2 `intrusion_detection_alert` events.
4. **Scenario 4 — Perimeter Firewall Decisions:** Inspected network connection records across source/destination IPs and ports, comparing `network_connection_blocked` (`198.51.100.20:443`) against `network_connection_allowed` (`198.51.100.50:80`).
5. **Scenario 5 — Temporal Activity Reconstruction:** Mapped all 8 events across 1-hour time buckets (`span=1h`) to inspect event clustering and outcome velocity.

---

## 9. Dashboard

I built **Security Operations Overview — Training Environment** (`Shared in App`) to unify key investigation metrics into a three-band SOC triage layout (documented in `dashboards/dashboard_design.md` and captured in `screenshots/12_dashboard_overview.png`):

- **Top Band (Headline KPI):**
  1. **Total Events** (`Single Value`) — Confirms active ingestion volume (`8` events) in `cybersecurity_lab`.
- **Middle Band (Trends & Comparisons):**
  2. **Event Volume Over Time** (`Line Chart`) — Hourly event cadence (`span=1h`).
  3. **Authentication Outcomes** (`Column Chart`) — Compares `failure` (`2`) vs. `success` (`2`) login events.
  4. **Firewall Decisions** (`Column Chart`) — Ranks counts across `event.action` values.
- **Bottom Band (Granular Drill-Down Tables):**
  5. **Failed Authentication by User** (`Statistics Table`) — Highlights `alex` (`2` failed attempts).
  6. **Failed Authentication by Source** (`Statistics Table`) — Links `192.0.2.25` to `2` failed attempts across `1` unique account.
  7. **DNS Activity** (`Statistics Table`) — Summarizes network-category actions (`intrusion_detection_alert`, `network_connection_allowed`, `network_connection_blocked`).

---

## 10. Findings

1. **Authentication Anomalies:** Two `authentication_failure` events occurred for user `alex` originating from documentation-range IP `192.0.2.25` (`unique_accounts = 1`), alongside two `authentication_success` events in the dataset.
2. **Perimeter & IDS Signals:** Suricata generated two `intrusion_detection_alert` events (`event.outcome="detected"`) at `08:03:00` and `08:08:00` UTC, while firewall telemetry recorded one blocked outbound HTTPS connection (`192.0.2.25 -> 198.51.100.20:443`) and one allowed outbound HTTP connection (`192.0.2.50 -> 198.51.100.50:80`).
3. **Schema Extraction Discovery:** Initial queries filtering on unquoted `event.category="authentication"` returned `0` events because Splunk extracted the JSON array as `"event.category{}"`. Inspecting raw events and `fieldsummary` resolved the issue and reinforced why schema verification always comes before complex SPL.

---

## 11. Limitations

- **Synthetic Small-Scale Dataset:** The 8-event sample in `normalised_events.jsonl` validates SPL mechanics, field extraction, and dashboard design, but does not represent enterprise traffic volume or statistical baseline variance.
- **Leads Are Not Proof of Compromise:** Two failed logins from a single IP or a blocked firewall connection are triage leads—not proof of brute-force takeover or malicious intent—without corroborating endpoint process logs, user context, and session correlation.
- **Missing DNS Payload Records:** No DNS query/response logs (`dns.question.name`) were present in this batch, so the dashboard's **DNS Activity** panel summarizes available `"event.category{}"="network"` actions instead.
- **Static Time Window:** Because sample timestamps sit on `2026-11-06`, queries must use **All time** rather than rolling windows like `Last 24 hours`.

---

## 12. Lessons Learned

- **Filter Early, Aggregate Late:** Placing `index=cybersecurity_lab` and attribute filters before `stats` or `timechart` keeps granular event fields available when needed and keeps searches efficient.
- **Always Set `span` in `timechart`:** Explicitly defining temporal buckets (`span=1h`) avoids inconsistent auto-bucketing across varying time ranges.
- **Verify Fields Before Building Queries:** Checking how Splunk extracts JSON arrays (`"event.category{}"`) and optional fields prevents silent zero-result queries.
- **Searching vs. Detection Engineering:** Running a search answers an ad-hoc question; building a production detection requires accounting for data coverage, event quality, baselines, benign operational noise, false-positive rates, grouping/suppression, and clear escalation steps.

---

## 13. Future Improvements

1. **Sigma Rule Translation (Day 23):** Convert key hunt scenarios—such as repeated authentication failures and IDS alert correlation—into vendor-neutral **Sigma** detection rules with defined severity, false-positive notes, and triage steps.
2. **Enrich Telemetry Coverage:** Expand the synthetic log generator to include DNS query logs (`dns.question.name`), endpoint process creation events (`process.name`, `process.command_line`), and multi-hour baselines.
3. **Dashboard Drilldowns & Input Tokens:** Add interactive Splunk dashboard time-range and `source.ip` dropdown tokens so analysts can click a source IP in a summary table and filter surrounding panels automatically.
4. **Automated Ingestion & Alerting:** Transition from manual JSONL file uploads to monitored directory inputs or Universal Forwarder simulation, paired with scheduled alerts and throttling rules.