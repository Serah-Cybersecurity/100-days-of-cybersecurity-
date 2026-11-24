# Structured SPL Search Records & Investigation Audit Log

**Author:** Serah Kathini Mulwa  
**Program:** Women Techsters Fellowship — Cybersecurity Track  
**Module:** Day 22 — Splunk Fundamentals & Search Processing Language (SPL)  
**Target Index:** `cybersecurity_lab` (`sourcetype="_json"`)  
**Dataset:** `normalised_events.jsonl` (8 normalized Elastic Common Schema events)

---

## 1. Why I Record Searches in a Structured Format

A raw list of SPL commands without context is nearly impossible to audit later. When I return to a repository weeks later—or when a hiring manager or teammate reviews my investigation—seeing only `| stats count by source.ip` leaves too many unanswered questions: *What time window did I search? What exact numbers came back? How did I interpret them, and what did I avoid assuming?*

Using a consistent **8-part investigation record** (`Objective`, `SPL`, `Data Source`, `Time Range`, `Results`, `Interpretation`, `Limitations`, and `Next Investigation Step`) keeps every hunt reproducible, transparent, and grounded in evidence rather than guesswork.

---

## 2. Standard 8-Part Search Record Template

```markdown
## Search: [Investigation Title]

### Objective
[State the specific security or auditing question this search answers.]

### SPL
```spl
[Insert exact SPL query executed]
```

### Data Source
`cybersecurity_lab`

### Time Range
[Record the exact time picker setting or earliest/latest window]

### Results
[Record the actual output returned by Splunk]

### Interpretation
[Explain what the observed results suggest as an investigative lead]

### Limitations
[Explain what the results cannot prove and any dataset/schema constraints]

### Next Investigation Step
[State what additional telemetry, correlation, or context would be checked next]
```

---

## 3. Executed Search Records (`cybersecurity_lab`)

## Search: Authentication Activity Baseline & Outcomes

### Objective
Measure baseline authentication volume and compare `success` versus `failure` outcomes across endpoint login events.

### SPL
```spl
index=cybersecurity_lab "event.category{}"="authentication"
| stats count by event.outcome
| sort - count
```

### Data Source
`cybersecurity_lab` (`normalised_events.jsonl`, `sourcetype="_json"`)

### Time Range
`All time` (synthetic dataset events timestamped `2026-11-06T08:00:00Z` – `2026-11-06T08:10:00Z`)

### Results
* `failure`: `2` events
* `success`: `2` events
* **Total authentication events:** `4` out of `8` total indexed events (`50%` failure rate in this sample window)

### Interpretation
Half of the authentication records in the sample window resulted in failures, while the other half succeeded. Seeing both outcomes present in the same short timeframe is a clear prompt to inspect which accounts and source IP addresses generated the failures and whether any successful logins followed them.

### Limitations
* **Schema Dependency:** Initial tests filtering on unquoted `event.category="authentication"` returned `0` events because Splunk extracted the JSON array field as `"event.category{}"`.
* **No Attribution Yet:** Outcome totals alone do not show which user accounts or source IPs were involved, and a 50% failure ratio in a tiny 4-event synthetic sample does not reflect a production baseline.

### Next Investigation Step
Group failed authentication events by `user.name` and `source.ip` to identify targeted accounts and originating addresses, then check timestamps to see whether failures preceded a successful login.

---

## Search: Failed Authentication by User

### Objective
Identify which user accounts experienced the highest number of failed authentication attempts.

### SPL
```spl
index=cybersecurity_lab "event.category{}"="authentication" event.outcome="failure"
| stats count by user.name
| sort - count
```

### Data Source
`cybersecurity_lab` (`normalised_events.jsonl`, `sourcetype="_json"`)

### Time Range
`All time` (synthetic dataset events timestamped `2026-11-06T08:00:00Z` – `2026-11-06T08:10:00Z`)

### Results
| `user.name` | `count` |
| :--- | :--- |
| `alex` | `2` |

### Interpretation
All observed failed authentication attempts (`2` events) targeted a single account (`alex`). Concentrated failures against one user account point toward either focused password guessing against that account or benign user/client friction (such as mistyped credentials, an expired password, or a misconfigured script).

### Limitations
* **Leads Are Not Proof:** Two failed login records prove that authentication failed twice for `alex`—they do not prove unauthorized access or malicious intent.
* **Field Completeness:** If any failed authentication event lacked a populated `user.name` field, `stats count by user.name` would exclude that record from the table unless missing values were normalized with `coalesce()`.

### Next Investigation Step
Check `source.ip` attribution for `alex`'s failed logins, inspect `alex`'s successful authentication events in the same window, and review host/endpoint context.

---

## Search: Failed Authentication by Source

### Objective
Identify originating IP addresses associated with failed authentication events and measure how many distinct accounts each source targeted.

### SPL
```spl
index=cybersecurity_lab "event.category{}"="authentication" event.outcome="failure"
| stats count AS failed_attempts dc(user.name) AS unique_accounts by source.ip
| sort - failed_attempts
```

### Data Source
`cybersecurity_lab` (`normalised_events.jsonl`, `sourcetype="_json"`)

### Time Range
`All time` (synthetic dataset events timestamped `2026-11-06T08:00:00Z` – `2026-11-06T08:10:00Z`)

### Results
| `source.ip` | `failed_attempts` | `unique_accounts` |
| :--- | :--- | :--- |
| `192.0.2.25` | `2` | `1` |

### Interpretation
A single documentation-range source IP (`192.0.2.25`) generated `2` failed authentication events against `1` distinct account (`alex`) during the test window. Pairing `failed_attempts` with `unique_accounts` (`dc(user.name)`) helps separate focused single-account retries (`unique_accounts = 1`) from multi-account password spraying (`unique_accounts > 1`), making this a targeted triage lead worth checking alongside successful logins and host context.

### Limitations
* **Sample Size & Synthetic Scope:** A small count from a synthetic lab dataset does not prove a brute-force attack, credential compromise, or malicious intent.
* **Network Translation Caveats:** In real environments, a `source.ip` can sit behind NAT gateways, proxies, or VPNs (hiding multiple legitimate users behind one IP), or an attacker can rotate across multiple source IPs.

### Next Investigation Step
Correlate authentication successes from `192.0.2.25` and `alex`, check whether `192.0.2.25` appears in perimeter firewall or Suricata IDS alerts, and inspect whether the failures clustered within seconds or minutes.

---

## Search: DNS & Intrusion Detection Telemetry Audit

### Objective
Audit DNS query telemetry (`dns.question.name`) and inspect network intrusion detection system (NIDS) alerts inside `cybersecurity_lab`.

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
`All time` (synthetic dataset events timestamped `2026-11-06T08:00:00Z` – `2026-11-06T08:10:00Z`)

### Results
* **DNS Query Check (`dns.question.name`):** `0` results returned (confirming DNS query payload fields are absent from this 8-event sample batch).
* **Intrusion Detection Audit (`intrusion_detection_alert`):** `2` events returned:

| `_time` | `host.name` | `event.provider` | `event.action` | `event.outcome` |
| :--- | :--- | :--- | :--- | :--- |
| `2026-11-06 08:03:00` | `null` | `suricata` | `intrusion_detection_alert` | `detected` |
| `2026-11-06 08:08:00` | `null` | `suricata` | `intrusion_detection_alert` | `detected` |

### Interpretation
Documenting the `0`-result DNS search honestly confirms a dataset coverage boundary rather than a broken query. Pivoting to network detection records revealed two Suricata IDS alerts (`event.outcome="detected"`) five minutes apart, indicating network traffic matched an IDS detection signature during the investigation window.

### Limitations
* **Signature Match vs. Exploit Success:** An IDS alert with `event.outcome="detected"` proves a rule pattern matched network traffic—it does not prove an exploit succeeded or that an endpoint was compromised.
* **Missing Host Context:** `host.name` is `null` on these network sensor records, and full signature names/IDs or packet payloads are not included in this summary table.

### Next Investigation Step
Expand the raw JSON fields for both Suricata events (`source.ip`, `destination.ip`, `destination.port`, `raw_reference`) and cross-reference those IPs against firewall connection logs and authentication activity.

---

## Search: Perimeter Firewall Connection Decisions

### Objective
Inspect network connection records across source/destination IP addresses and ports to evaluate allowed versus blocked perimeter decisions.

### SPL
```spl
index=cybersecurity_lab event.action=*network*
| table _time source.ip destination.ip destination.port event.action
```

### Data Source
`cybersecurity_lab` (`normalised_events.jsonl`, `sourcetype="_json"`)

### Time Range
`All time` (synthetic dataset events timestamped `2026-11-06T08:00:00Z` – `2026-11-06T08:10:00Z`)

### Results
| `_time` | `source.ip` | `destination.ip` | `destination.port` | `event.action` |
| :--- | :--- | :--- | :--- | :--- |
| `2026-11-06 08:02:00` | `192.0.2.25` | `198.51.100.20` | `443` | `network_connection_blocked` |
| `2026-11-06 08:07:00` | `192.0.2.50` | `198.51.100.50` | `80` | `network_connection_allowed` |

### Interpretation
Two notable investigative leads appear in the network connection table:
1. `192.0.2.25`—the same source IP associated with the two failed login attempts for `alex`—attempted an outbound connection to `198.51.100.20` on TCP port `443` at `08:02:00`, which was blocked (`network_connection_blocked`).
2. `192.0.2.50` established an allowed unencrypted HTTP connection (`destination.port=80`) to `198.51.100.50` at `08:07:00`.

### Limitations
* **Policy Block vs. Threat Confirmation:** A blocked connection shows perimeter policy enforcement worked for that attempt, not why the host initiated the traffic. Similarly, an allowed port `80` connection may be routine web traffic or an unencrypted check-in requiring payload/reputation context.
* **Synthetic Documentation IPs:** Both `192.0.2.0/24` and `198.51.100.0/24` are RFC 5737 documentation ranges used safely for lab modeling.

### Next Investigation Step
Correlate `192.0.2.25` across all `8` events in `cybersecurity_lab` to build a single-entity timeline covering its blocked `443` connection (`08:02`), Suricata alert (`08:03`), and authentication failures.

---

## Search: Temporal Event Volume & Outcome Trends

### Objective
Reconstruct event cadence and compare outcome distributions over explicit one-hour time buckets.

### SPL
```spl
index=cybersecurity_lab
| timechart span=1h count by event.outcome
```

### Data Source
`cybersecurity_lab` (`normalised_events.jsonl`, `sourcetype="_json"`)

### Time Range
`All time` (synthetic dataset events timestamped `2026-11-06T08:00:00Z` – `2026-11-06T08:10:00Z`)

### Results
| `_time` | `allowed` | `denied` | `detected` | `failure` | `success` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `2026-11-06 08:00` | `1` | `1` | `2` | `2` | `2` |

### Interpretation
All `8` events across the dataset fall within the `2026-11-06 08:00` hourly bucket, showing simultaneous authentication, firewall, and Suricata activity within a 10-minute operational window. Explicitly defining `span=1h` ensures consistent bucket sizing when comparing volume across dashboards and reports.

### Limitations
* **Bucket Granularity:** A `1h` span groups all events from `08:00` to `08:59` into a single row, smoothing out the exact minute-by-minute order of events inside that hour.
* **When vs. Why:** A timechart shows *when* activity clustered, not *why* it occurred—root-cause analysis always requires drilling back into underlying event records.

### Next Investigation Step
Run a narrower time-bucketed view (`span=1m` or `span=5m`) or sort individual events chronologically by `_time` (`| table _time observer.type event.action event.outcome source.ip destination.ip user.name | sort _time`) to verify the exact sequence of activity between `08:00` and `08:10`.