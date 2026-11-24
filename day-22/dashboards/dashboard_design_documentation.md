# Security Operations Overview — Training Environment

## 1. Dashboard Metadata & Environment Overview

- **Dashboard Title:** `Security Operations Overview — Training Environment`
- **Dashboard ID:** `security_operations_overview__training_environment`
- **Description:** Centralized threat-hunting overview tracking authentication anomalies, network traffic, firewall decisions, and ingestion volumes.
- **Permissions / Scope:** `Shared in App`
- **Target Index:** `cybersecurity_lab`
- **Source Dataset:** `normalised_events.jsonl` (ingested via Splunk Web on Splunk Enterprise running on a Parrot OS virtual machine)
- **Recommended Time Range:** **All time** (for static training/sample datasets; switch to rolling windows such as `Last 24 hours` or `Last 7 days` for live streaming telemetry)
- **Visual Reference:** `screenshots/day22-dashboard-overview.png`

---

## 2. Data Ingestion, Field Extraction & Schema Notes

When `normalised_events.jsonl` is indexed into `cybersecurity_lab` using `_json` source type extraction, nested JSON objects and arrays are mapped into dotted and multi-value Splunk field names:

- **Array Field Syntax (`"event.category{}"`):** Splunk extracts JSON array fields such as `event.category` with curly braces (`event.category{}`). Filtering or grouping by category should reference `"event.category{}"` rather than `event.category` so array elements are matched reliably.
- **Observed Categories & Outcomes in Sample Dataset:**
  - `"event.category{}"="authentication"` with `event.outcome` values `failure` (`authentication_failure`) and `success` (`authentication_success`)
  - `"event.category{}"="network"` with `event.outcome` / `event.action` values including `network_connection_allowed`, `network_connection_blocked`, and `intrusion_detection_alert`
- **Multi-Field `stats` Grouping Caution:** When running ad-hoc `stats` queries across multiple fields (`stats count by fieldA, fieldB, fieldC`), Splunk only includes events where all grouped fields are present on the same event. Keep group-by lists scoped to fields relevant to the specific event subset.

---

## 3. Top-to-Bottom Dashboard Layout Architecture

The dashboard is structured into three clear horizontal bands from top to bottom so analysts see high-level volume first, trend/distribution charts in the middle, and granular investigation tables at the bottom:

1. **Top Band (KPI Summary):**
   - **Total Events** (`Single Value`)
2. **Middle Band (Trends, Outcomes & Decisions):**
   - **Event Volume Over Time** (`Line Chart`)
   - **Authentication Outcomes** (`Column Chart`)
   - **Firewall Decisions** (`Column Chart`)
3. **Bottom Band (Granular Investigation Tables):**
   - **Failed Authentication by User** (`Statistics Table`)
   - **Failed Authentication by Source** (`Statistics Table`)
   - **DNS Activity** (`Statistics Table`)

---

## 4. Detailed Panel Specifications

### Panel 1: Total Events
- **Layout Position:** Top Band (KPI Card)
- **Visualization Type:** Single Value
- **SPL Query:**
  ```spl
  index=cybersecurity_lab | stats count
  ```
- **Operational Purpose:** Provides an immediate headline count of total normalized security events ingested into `cybersecurity_lab` over the selected time range, confirming data flow and establishing baseline scale before diving into specific categories.
- **Interpreting Spikes & Anomalies:** A sudden jump in total events can indicate a burst of scanner/brute-force noise, an IDS/firewall alert storm, a newly enabled log source, or duplicate ingestion. A drop to `0` or an unexpected flatline during active lab/telemetry periods points to ingestion delays, forwarder/upload issues, or an overly narrow time filter.
- **Limitations:** Aggregates every event in `cybersecurity_lab` indiscriminately—it does not distinguish high-severity alerts from routine allowed traffic, nor does it validate field completeness or timestamp accuracy.

---

### Panel 2: Event Volume Over Time
- **Layout Position:** Middle Band (Trend Chart)
- **Visualization Type:** Line Chart
- **SPL Query:**
  ```spl
  index=cybersecurity_lab | timechart span=1h count
  ```
- **Operational Purpose:** Visualizes event ingestion and activity cadence across hourly buckets (`span=1h`) to spot temporal clustering, off-hours activity, and ingestion gaps.
- **Interpreting Spikes & Anomalies:** Sharp hourly peaks or off-hours activity clusters warrant correlation with authentication failures, firewall blocks, or IDS alerts during the same time window. Empty intervals or steps can reflect sparse sample timestamps, time-range boundaries, or collection interruptions.
- **Limitations:** Fixed `span=1h` bucketing can smooth out short, high-intensity bursts (such as a rapid 2-minute brute-force script) and may appear flat or single-point when sample events share identical or closely spaced timestamps.

---

### Panel 3: Authentication Outcomes
- **Layout Position:** Middle Band (Comparison Chart)
- **Visualization Type:** Column Chart
- **SPL Query:**
  ```spl
  index=cybersecurity_lab "event.category{}"="authentication" | stats count by event.outcome | sort - count
  ```
- **Operational Purpose:** Compares authentication event outcomes (`failure` vs. `success`) across authentication records to give analysts a quick ratio of rejected vs. successful logins.
- **Interpreting Spikes & Anomalies:** A high volume or sudden spike in `failure` events suggests credential guessing, password spraying, misconfigured service accounts, or expired tokens. A `success` event occurring right alongside or immediately after a wave of `failure` events is a high-priority lead to investigate for potential account compromise.
- **Limitations:** Depends on accurate normalization of `"event.category{}"="authentication"` and `event.outcome`. Outcome counts alone do not reveal *which* user accounts or source IPs were involved, nor do they prove whether a `success` was legitimate or unauthorized.

---

### Panel 4: Firewall Decisions
- **Layout Position:** Middle Band (Action Distribution Chart)
- **Visualization Type:** Column Chart
- **SPL Query:**
  ```spl
  index=cybersecurity_lab | stats count by event.action | sort - count
  ```
- **Operational Purpose:** Breaks down event counts by `event.action` across `cybersecurity_lab` so analysts can see the distribution of allowed connections, blocked connections, authentication actions, and intrusion detection alerts at a glance.
- **Interpreting Spikes & Anomalies:** Elevated counts of blocked/denied actions (`network_connection_blocked`) or intrusion detection alerts (`intrusion_detection_alert`) can indicate port scanning, lateral movement probes, or policy violations. Conversely, an unexpected surge in allowed actions (`network_connection_allowed`) to unusual destinations or ports warrants closer review.
- **Limitations:** Because this query groups by `event.action` across `index=cybersecurity_lab` without restricting to a single log source or action subset, it includes non-firewall actions (such as authentication actions or IDS alerts) if present in `event.action`. Long action names can also be visually truncated in narrow column chart labels.

---

### Panel 5: Failed Authentication by User
- **Layout Position:** Bottom Band (Investigation Table)
- **Visualization Type:** Statistics Table
- **SPL Query:**
  ```spl
  index=cybersecurity_lab "event.category{}"="authentication" event.outcome="failure" | stats count by user.name | sort - count
  ```
- **Operational Purpose:** Ranks targeted user accounts (`user.name`) by number of failed authentication attempts in descending order so analysts can spot targeted accounts or recurring lockouts.
- **Interpreting Spikes & Anomalies:** High failure counts on a single privileged, service, or high-value account point toward targeted brute-force attempts or a stuck credential/automation job. Repeated failures across many distinct usernames point toward password spraying or enumeration.
- **Limitations:** Failed login counts indicate *attempted* authentication failures—not confirmed account compromise. Missing or inconsistent `user.name` values (or alias variations for the same identity) can split or omit rows.

---

### Panel 6: Failed Authentication by Source
- **Layout Position:** Bottom Band (Investigation Table)
- **Visualization Type:** Statistics Table
- **SPL Query:**
  ```spl
  index=cybersecurity_lab "event.category{}"="authentication" event.outcome="failure" | stats count AS failed_attempts dc(user.name) AS unique_accounts by source.ip | sort - failed_attempts
  ```
- **Operational Purpose:** Aggregates failed authentications by originating IP (`source.ip`), pairing total `failed_attempts` with distinct targeted accounts (`unique_accounts`) to help distinguish single-target brute force from multi-account password spraying or distributed scanners.
- **Interpreting Spikes & Anomalies:**
  - **High `failed_attempts` + low `unique_accounts` (e.g., `1`):** Often indicates focused brute-force guessing against a specific account or a misconfigured client/service retrying bad credentials.
  - **High `failed_attempts` + high `unique_accounts`:** Strongly suggests credential stuffing or password spraying across multiple accounts from a single source.
- **Limitations:** Source IP addresses can be masked behind NAT gateways, proxies, VPNs, or load balancers—meaning a busy shared IP may represent multiple legitimate users rather than one attacker, while an adversary may rotate across many IPs. Also, `dc(user.name)` only counts events where `user.name` is populated.

---

### Panel 7: DNS Activity
- **Layout Position:** Bottom Band (Investigation Table)
- **Visualization Type:** Statistics Table
- **SPL Query:**
  ```spl
  index=cybersecurity_lab "event.category{}"="network" | stats count by event.action | sort - count
  ```
- **Operational Purpose:** Surfaces network-category activity grouped by `event.action` within `index=cybersecurity_lab` to review connection allowances, blocks, and detection alerts alongside network traffic behavior.
- **Interpreting Spikes & Anomalies:** Unusual spikes in specific network actions—such as `intrusion_detection_alert` or `network_connection_blocked`—warrant pivoting to source/destination IPs, ports, and timestamps for deeper triage.
- **Limitations:** In the current 8-event `normalised_events.jsonl` training sample, network records represent connection and IDS events (`network_connection_allowed`, `network_connection_blocked`, `intrusion_detection_alert`) rather than dedicated DNS query/response logs, and grouping solely by `event.action` does not show queried domain names, record types, or destination hosts.

---

## 5. Screenshot & Verification Checklist

- [x] Dashboard created as **Security Operations Overview — Training Environment** with `Shared in App` permissions
- [x] Array category field handled via `"event.category{}"`
- [x] All 7 panels configured, mapped to `index=cybersecurity_lab`, and arranged top-to-bottom (`Total Events` at top, charts in middle, tables at bottom)
- [x] **Firewall Decisions** verified rendering non-empty counts
- [ ] Final dashboard screenshot saved at `screenshots/day22-dashboard-overview.png`
- [ ] Design documentation saved at `dashboards/dashboard_design.md`