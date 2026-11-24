# Security Operations Overview — Training Environment

**Author:** Serah Kathini Mulwa  
**Program:** Women Techsters Fellowship — Cybersecurity Track  
**Module:** Day 22 — Splunk Fundamentals & Search Processing Language (SPL)  
**Target Index:** `cybersecurity_lab` (`sourcetype="_json"`)  
**Visual Reference:** `screenshots/day22-dashboard-overview.png`

---

## 1. Dashboard Overview & Operational Purpose

I designed **Security Operations Overview — Training Environment** as a centralized threat-hunting and triage view for my Day 22 Splunk investigation workbench. Instead of throwing random charts onto a screen just because Splunk can render them, I built every panel to answer a specific operational question: *How much data is flowing into the lab index? What is happening with authentication? Are network connections being allowed or blocked? And where should I look next as a SOC analyst?*

- **Dashboard Title:** `Security Operations Overview — Training Environment` *(displayed in Splunk Web header as `Security Operations Overview - Training Environment`)*
- **Dashboard ID:** `security_operations_overview__training_environment`
- **Permissions / Scope:** `Shared in App`
- **Target Index:** `cybersecurity_lab`
- **Source Dataset:** `normalised_events.jsonl` (8 normalized Elastic Common Schema events carried over from the Day 21 Python Mini-SIEM pipeline and uploaded via Splunk Web into the `cybersecurity_lab` index)
- **Recommended Time Range:** **All time** for static lab/training events (switch to rolling windows such as `Last 24 hours` or `Last 7 days` when monitoring live streaming telemetry)
- **Visual Reference:** `screenshots/day22-dashboard-overview.png`

---

## 2. Schema Extraction & SPL Quirks I Ran Into

Testing queries directly against `normalised_events.jsonl` after indexing with `sourcetype="_json"` taught me a few practical details about how Splunk handles normalized JSON fields:

- **JSON Array Field Syntax (`"event.category{}"`):** Splunk extracts array fields like `event.category` with curly braces (`event.category{}`). Using `"event.category{}"` when filtering or grouping matches array elements reliably instead of missing multi-value or nested array entries.
- **What Appears in This Sample Dataset:**
  - `"event.category{}"="authentication"` includes events with `event.outcome` values of `failure` (`authentication_failure`) and `success` (`authentication_success`).
  - `"event.category{}"="network"` includes network and detection records such as `network_connection_allowed`, `network_connection_blocked`, and `intrusion_detection_alert`.
- **Multi-Field `stats` Grouping Behavior:** When grouping with `stats count by fieldA, fieldB, fieldC`, Splunk only includes events where *every* grouped field exists on that event. To avoid accidentally hiding valid records that lack optional fields, I keep each panel's `by` clause focused on fields that actually belong to that subset of events.

---

## 3. Top-to-Bottom Dashboard Layout

I organized the dashboard from top to bottom following a standard SOC triage flow—starting with high-level ingestion health, moving into trend and outcome comparisons, and ending with specific tables for analyst drill-down:

1. **Top Band — Headline KPI:**
   - **Total Events** (`Single Value`)
2. **Middle Band — Trends, Outcomes & Decisions:**
   - **Event Volume Over Time** (`Line Chart`)
   - **Authentication Outcomes** (`Column Chart`)
   - **Firewall Decisions** (`Column Chart`)
3. **Bottom Band — Investigation Tables:**
   - **Failed Authentication by User** (`Statistics Table`)
   - **Failed Authentication by Source** (`Statistics Table`)
   - **DNS Activity** (`Statistics Table`)

---

## 4. Panel-by-Panel Specifications

### Panel 1: Total Events
- **Layout Position:** Top Band (Single Value KPI)
- **Visualization Type:** Single Value
- **SPL Query:**
  ```spl
  index=cybersecurity_lab | stats count
  ```
- **Purpose:** Gives an immediate count of all normalized events inside `cybersecurity_lab` for the chosen time window so I know right away that data is indexed and searchable.
- **How I Interpret Results & Spikes:** A sudden jump in event volume can point to noisy authentication retries, firewall blocks, IDS alerts, or a fresh log batch upload. A `0` or flatline during an active check usually means the wrong time picker range is selected, the index name is off, or data hasn't finished indexing.
- **Limitations:** It is a raw total across everything in `cybersecurity_lab`. It does not separate high-signal alerts from routine events or tell me whether timestamps and fields were parsed cleanly.

---

### Panel 2: Event Volume Over Time
- **Layout Position:** Middle Band (Line Chart)
- **Visualization Type:** Line Chart
- **SPL Query:**
  ```spl
  index=cybersecurity_lab | timechart span=1h count
  ```
- **Purpose:** Tracks event volume across one-hour buckets (`span=1h`) so I can see when activity clusters or drops off over time.
- **How I Interpret Results & Spikes:** Spikes or unusual off-hours activity are prompts to check authentication failures, blocked connections, and IDS alerts during that exact time window. Sparse points or flat stretches reflect how timestamps are distributed in the dataset or time-range boundaries.
- **Limitations:** Using `span=1h` smooths out short bursts—for example, a fast brute-force script running over three minutes inside a single hour won't show minute-by-minute peaks here. In a small sample dataset with events clustered around one timestamp, the chart can look minimal.

---

### Panel 3: Authentication Outcomes
- **Layout Position:** Middle Band (Column Chart)
- **Visualization Type:** Column Chart
- **SPL Query:**
  ```spl
  index=cybersecurity_lab "event.category{}"="authentication" | stats count by event.outcome | sort - count
  ```
- **Purpose:** Compares `failure` versus `success` counts across authentication events so I can quickly spot abnormal failure ratios.
- **How I Interpret Results & Spikes:** Elevated `failure` counts can point to password guessing, password spraying, expired credentials, or a broken service script. If a `success` shows up right alongside or right after a burst of failures, that is a strong lead to investigate further.
- **Limitations:** This panel relies on clean normalization of `"event.category{}"="authentication"` and `event.outcome`. Outcome totals alone do not show which user or IP was involved, and a successful login is not automatically malicious or automatically safe without context.

---

### Panel 4: Firewall Decisions
- **Layout Position:** Middle Band (Column Chart)
- **Visualization Type:** Column Chart
- **SPL Query:**
  ```spl
  index=cybersecurity_lab | stats count by event.action | sort - count
  ```
- **Purpose:** Displays counts across `event.action` values in `cybersecurity_lab` so I can see allowed connections, blocked connections, authentication outcomes, and IDS alerts side by side.
- **How I Interpret Results & Spikes:** More `network_connection_blocked` or `intrusion_detection_alert` events can signal scanning, policy denials, or rule hits worth inspecting. An unusual spike in `network_connection_allowed` events to unexpected destinations or ports also deserves a closer look.
- **Limitations:** Because this query groups by `event.action` across `index=cybersecurity_lab` rather than filtering strictly to firewall/connection events, it includes non-firewall actions if they exist in `event.action`. Also, on a narrower column chart, longer action names get truncated along the horizontal axis (as seen in `screenshots/day22-dashboard-overview.png`), so I pair this chart with raw event or table lookups when reading full action names.

---

### Panel 5: Failed Authentication by User
- **Layout Position:** Bottom Band (Statistics Table)
- **Visualization Type:** Statistics Table
- **SPL Query:**
  ```spl
  index=cybersecurity_lab "event.category{}"="authentication" event.outcome="failure" | stats count by user.name | sort - count
  ```
- **Purpose:** Ranks user accounts (`user.name`) from highest to lowest failed authentication count to highlight accounts seeing repeated login failures.
- **How I Interpret Results & Spikes:** High failures on a single account (such as `alex` in the sample dataset) can indicate targeted guessing against that account or a misconfigured client/automation job. Failures spread across many different usernames point more toward password spraying or account enumeration.
- **Limitations:** A failed login count is an investigative lead, not proof that an account was compromised. If `user.name` is missing on some events or formatted inconsistently across sources, counts can be split or omitted.

---

### Panel 6: Failed Authentication by Source
- **Layout Position:** Bottom Band (Statistics Table)
- **Visualization Type:** Statistics Table
- **SPL Query:**
  ```spl
  index=cybersecurity_lab "event.category{}"="authentication" event.outcome="failure" | stats count AS failed_attempts dc(user.name) AS unique_accounts by source.ip | sort - failed_attempts
  ```
- **Purpose:** Groups failed authentications by `source.ip` and pairs `failed_attempts` with `unique_accounts` (`dc(user.name)`) to help distinguish single-account retries/brute force from multi-account spraying.
- **How I Interpret Results & Spikes:** A source IP with high `failed_attempts` and a low `unique_accounts` count (such as `1`) suggests focused attempts against one account or a bad credential loop. High `failed_attempts` paired with a high `unique_accounts` count points toward spraying or scanning across multiple accounts.
- **Limitations:** A `source.ip` can sit behind NAT, a proxy, a VPN, or a shared gateway, meaning multiple users may share one IP—or an attacker may rotate across multiple IPs. Also, `dc(user.name)` only reflects events where `user.name` is present.

---

### Panel 7: DNS Activity
- **Layout Position:** Bottom Band (Statistics Table)
- **Visualization Type:** Statistics Table
- **SPL Query:**
  ```spl
  index=cybersecurity_lab "event.category{}"="network" | stats count by event.action | sort - count
  ```
- **Purpose:** Summarizes network-category events by `event.action` inside `index=cybersecurity_lab` to highlight connection allowances, blocks, and detection alerts.
- **How I Interpret Results & Spikes:** Spikes in `intrusion_detection_alert` or `network_connection_blocked` warrant pivoting to source/destination IPs, ports, and timestamps to see what traffic triggered them.
- **Limitations:** In my current 8-event `normalised_events.jsonl` sample, network events consist of connection and Suricata alert records (`intrusion_detection_alert`, `network_connection_allowed`, `network_connection_blocked`) rather than dedicated DNS query/response logs, and grouping only by `event.action` does not show domain names (`dns.question.name`) or response codes. Once DNS query logs are included in future datasets, I can extend this panel to inspect queried domains and record types directly.

---

## 5. Verification & Readiness Checklist

- [x] Dashboard created as **Security Operations Overview — Training Environment** (`Shared in App`)
- [x] Array category field handled cleanly using `"event.category{}"`
- [x] All 7 panels configured, scoped to `index=cybersecurity_lab`, and arranged top-to-bottom (`Total Events` at top, charts in middle, tables at bottom)
- [x] Verified panel rendering and documented known dataset and visualization limitations
- [x] Final dashboard screenshot saved at `screenshots/day22-dashboard-overview.png`
- [x] Design documentation saved at `dashboards/dashboard_design.md`