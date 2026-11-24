# Search Processing Language (SPL) Knowledge Reference

**Author:** Serah Kathini Mulwa

**Program:** Women Techsters Fellowship — Cybersecurity Track

**Module:** Day 22 — Splunk Fundamentals & Search Processing Language (SPL)

**Target Index:** `cybersecurity_lab` (`sourcetype="_json"`)

## 1. Why This Reference Exists

As I worked through my Day 22 investigation workbench, one thing became obvious: memorizing queries without understanding *how* each command shapes the data pipeline makes troubleshooting way harder than it needs to be. When a search returns `0` events or drops a field I expected to see, knowing what each command actually does—and where it belongs in a pipe chain—saves me from guessing.

This document is my practical SPL field guide covering the core commands I use for security telemetry analysis, threat hunting, and incident triage.

## 2. Quick Reference Table

| Command | Purpose | Example Use |
| :--- | :--- | :--- |
| `search` | Filter events | Find failed logins |
| `table` | Display selected fields | Show authentication details |
| `fields` | Retain or remove fields | Reduce field clutter |
| `sort` | Order results | Highest event counts first |
| `head` | Limit results | Inspect first 10 events |
| `dedup` | Remove duplicate results | Distinct source records |
| `stats` | Aggregate events | Count events by user |
| `eval` | Create calculated fields | Categorise outcomes |
| `where` | Filter using expressions | Filter numeric values |
| `timechart` | Analyse events over time | Hourly event volume |
| `fieldsummary` | Summarise field information | Understand the dataset |

---

## 3. Core Pipeline Habits Before You Query

Before diving into individual commands, three habits keep my SPL clean, accurate, and fast:

* **Filter Early, Aggregate Late:** Scope the index (`index=cybersecurity_lab`) and filter out irrelevant events at the start of the pipeline before running transforming commands like `stats` or `timechart`. Filtering early reduces how much data moves through the pipeline; aggregating late keeps granular fields available until you are ready to summarize them.
* **Inspect Real Schemas First:** Never assume field names or types match a tutorial example. On my Day 21 normalized JSONL dataset (`normalised_events.jsonl`), I had to check how nested fields and arrays (such as `"event.category{}"`) were extracted in Splunk rather than guessing.
* **Separate Observations from Conclusions:** Even a great SPL query only surfaces patterns or counts. Context from surrounding events, hosts, and time windows determines what those numbers actually mean.

---

## 4. Detailed Command Reference

### 1. `search`

#### 1. What It Does
`search` filters events from an index based on keywords, field-value pairs, wildcards, and boolean operators (`AND`, `OR`, `NOT`), and it can also filter results further later in a pipeline.

#### 2. Why an Analyst Uses It
An analyst uses `search` to narrow millions—or dozens—of log records down to the exact slice of telemetry relevant to a question, such as failed logins, specific source IPs, or particular event actions.

#### 3. Basic Syntax
```spl
index=<index_name> <field>=<value> [AND|OR|NOT ...]
```
*(After a pipe `|`, `| search <expression>` can also be used to filter already-processed pipeline results.)*

#### 4. Example
```spl
index=cybersecurity_lab event.action="authentication_failure"
```

#### 5. Common Mistake
Assuming field names or exact string values without checking the data first—for example, searching `event.category="authentication"` on a dataset where `event.category` is extracted as a JSON array (`"event.category{}"`) or where failures are recorded under a specific `event.action` value, leading to `0` results even when matching logs exist.

#### 6. Practical SOC Use Case
During an authentication triage check, I start with `search` to isolate failed login events inside `cybersecurity_lab` so I can inspect which accounts or source addresses are generating errors before aggregating or charting them.

---

### 2. `table`

#### 1. What It Does
`table` formats search results into a clean spreadsheet-style table showing only the specific fields you list, in the exact column order you specify.

#### 2. Why an Analyst Uses It
Raw log events are often crowded with dozens of metadata and nested JSON fields. `table` lets an analyst line up just the key investigation columns side by side to read timelines and relationships quickly.

#### 3. Basic Syntax
```spl
... | table <field1> <field2> <field3> ...
```

#### 4. Example
```spl
index=cybersecurity_lab event.action=*network*
| table _time source.ip destination.ip destination.port event.action
```

#### 5. Common Mistake
Using `table` too early right after an initial filter and then trying to run an aggregation that depends on fields you did not include—or forgetting that `table` creates a tabular output view rather than preserving raw event expansion for every field.

#### 6. Practical SOC Use Case
When reviewing network connection records, I use `table` to display `_time`, `source.ip`, `destination.ip`, `destination.port`, and `event.action` together so I can quickly compare allowed and blocked traffic across endpoints and ports.

---

### 3. `fields`

#### 1. What It Does
`fields` keeps only the specified fields (default) or removes specified fields (when prefixed with `-`) from events passing through the pipeline.

#### 2. Why an Analyst Uses It
Dropping unneeded fields—or keeping only relevant ones—reduces field clutter in the sidebar/results and cuts down unnecessary data transfer and processing overhead earlier in a search pipeline.

#### 3. Basic Syntax
```spl
... | fields [+|-] <field1>, <field2>, ...
```

#### 4. Example
```spl
index=cybersecurity_lab | fields - _raw
```

#### 5. Common Mistake
Accidentally stripping out a field you still need later in the query (such as removing `user.name` or `source.ip` before a `stats ... by` step), resulting in blank or missing groupings downstream.

#### 6. Practical SOC Use Case
When working with verbose JSON logs that carry extra metadata blocks I do not need for a quick check, I use `fields` to keep only the core fields I am inspecting so the output stays focused and readable.

---

### 4. `sort`

#### 1. What It Does
`sort` orders search results or statistical rows in ascending or descending order based on one or more fields, and can also limit how many sorted rows are returned.

#### 2. Why an Analyst Uses It
In threat hunting, outliers usually sit at the top or bottom of a list. `sort` puts the highest failure counts, busiest destinations, or most recent timestamps right where an analyst sees them first.

#### 3. Basic Syntax
```spl
... | sort [limit] [+|-]<field1>, [+|-]<field2>, ...
```
*(Prefixing a field with `-` sorts descending, such as highest counts first; `+` or no sign sorts ascending.)*

#### 4. Example
```spl
index=cybersecurity_lab
| stats count by event.action
| sort - count
```

#### 5. Common Mistake
Forgetting the minus sign (`-`) when you want largest-to-smallest counts—leaving `| sort count` in ascending order so `1` appears at the top and larger counts get buried below.

#### 6. Practical SOC Use Case
After counting events by `event.action` or ranking failed logins per source, I run `| sort - count` so the most frequent actions or highest-volume sources immediately appear at the top of my triage table.

---

### 5. `head`

#### 1. What It Does
`head` returns the first `N` results (defaulting to `10` if no number is given) from the incoming stream and stops processing further results once that limit is reached.

#### 2. Why an Analyst Uses It
When exploring a new index or testing whether a query matches anything, pulling a small sample like `1` or `10` events lets an analyst inspect real structure and field values fast without waiting on a huge output.

#### 3. Basic Syntax
```spl
... | head [<N>]
```

#### 4. Example
```spl
index=cybersecurity_lab | head 10
```

#### 5. Common Mistake
Running `| head 10` *after* an aggregation or forgetting that `head` only shows a small slice—leading a beginner to mistakenly think the total count in the dataset is `10` when there are actually more events behind it.

#### 6. Practical SOC Use Case
Right after ingesting `normalised_events.jsonl` into `cybersecurity_lab`, I use `head` to inspect sample events and confirm that timestamps, nested JSON objects, and observer fields look right before running broader queries.

---

### 6. `dedup`

#### 1. What It Does
`dedup` removes duplicate events that share the same value(s) for one or more specified fields, keeping the first matching event (or top `N` per group if specified) by default.

#### 2. Why an Analyst Uses It
Security logs often repeat the same connection attempt, alert, or status message across multiple lines. `dedup` strips repetitive noise so an analyst can see each distinct entity or pattern once.

#### 3. Basic Syntax
```spl
... | dedup [<N>] <field1> [<field2> ...]
```

#### 4. Example
```spl
index=cybersecurity_lab | dedup source.ip
```

#### 5. Common Mistake
Using `dedup` to count distinct items instead of `dc()` inside `stats`—for instance, running `| dedup source.ip` and treating the remaining row count as a full summary without noticing that `dedup` discards the underlying duplicate events and only keeps the first event seen for each IP.

#### 6. Practical SOC Use Case
When hunting across network or authentication logs, I use `dedup` to pull one representative event per `source.ip` or `user.name` so I can inspect the event structure of each distinct source without reading identical records over and over.

---

### 7. `stats`

#### 1. What It Does
`stats` calculates aggregate statistical metrics—such as `count`, distinct count (`dc()`), `sum`, `avg`, `min`, `max`, `values()`, `earliest()`, and `latest()`—across events, optionally grouped by one or more fields using `by`.

#### 2. Why an Analyst Uses It
`stats` turns raw event streams into structured summaries—showing how many times something happened, how many distinct accounts were touched, or which sources generated the most activity.

#### 3. Basic Syntax
```spl
... | stats <function>(<field>) [AS <alias>] [by <group_field1>, <group_field2> ...]
```

#### 4. Example
```spl
index=cybersecurity_lab event.action="authentication_failure"
| stats count AS failed_attempts dc(user.name) AS unique_accounts by source.ip
| sort - failed_attempts
```

#### 5. Common Mistake
Grouping by too many fields at once (`stats count by a, b, c, d`), which can split counts across sparse combinations or omit events where one of those fields is null/missing, or forgetting `AS` aliases when building clear dashboard tables.

#### 6. Practical SOC Use Case
To spot potential brute-force versus password-spraying behavior, I use `stats` to calculate both `failed_attempts` (`count`) and `unique_accounts` (`dc(user.name)`) grouped by `source.ip`.

---

### 8. `eval`

#### 1. What It Does
`eval` creates new calculated fields or overwrites existing field values using expressions, conditional logic (`if`, `case`), string/null helpers (`coalesce`, `lower`, `tonumber`), and math operations.

#### 2. Why an Analyst Uses It
Raw logs rarely label things in the exact way an investigation or dashboard needs. `eval` lets an analyst normalize values, classify outcomes, compute ratios or durations, and replace missing/null values cleanly.

#### 3. Basic Syntax
```spl
... | eval <new_or_existing_field> = <expression> [, <field2> = <expression2> ...]
```

#### 4. Example
```spl
index=cybersecurity_lab
| eval auth_status = if(event.action="authentication_failure", "failed_login", "other_or_success")
| stats count by auth_status
```

#### 5. Common Mistake
Forgetting quotes around string literals in expressions (writing `if(event.outcome=failure, ...)` instead of `if(event.outcome="failure", ...)`), or using `=` instead of `==` inside comparison functions like `if()` or `case()`, causing the expression to evaluate unexpectedly.

#### 6. Practical SOC Use Case
When raw event actions or outcomes have inconsistent labels across log sources, I use `eval` to categorize events into clear triage buckets (such as separating failed logins or flagging missing fields with `coalesce()`) so tables and charts are easier to read.

---

### 9. `where`

#### 1. What It Does
`where` filters events or statistical rows using `eval`-style boolean expressions and functions—supporting comparisons (`>`, `<`, `>=`, `<=`, `=`, `!=`), boolean logic (`AND`, `OR`, `NOT`), and functions like `isnotnull()` or `isnull()`.

#### 2. Why an Analyst Uses It
While `search` is great for keyword and field matching, `where` shines when filtering based on numeric thresholds, field-to-field comparisons, or functions after calculations or `stats` aggregations have run.

#### 3. Basic Syntax
```spl
... | where <boolean_expression>
```

#### 4. Example
```spl
index=cybersecurity_lab event.action="authentication_failure"
| stats count AS failed_attempts by source.ip
| where failed_attempts >= 2
```

#### 5. Common Mistake
Confusing `=` and `==` or forgetting that `where` evaluates expressions differently than `search`—for example, `where failed_attempts > 1` works cleanly on numeric `stats` output, whereas unquoted text strings without quotes or `like()`/`match()` can trip up beginners.

#### 6. Practical SOC Use Case
After aggregating failed authentications or connection attempts with `stats`, I use `where` to filter out single-event noise and focus only on sources or counts that meet a minimum threshold for closer review.

---

### 10. `timechart`

#### 1. What It Does
`timechart` creates a time-series aggregation with `_time` along the x-axis and statistical calculations (such as `count`, `dc()`, or `sum()`) bucketed across time intervals, optionally split into series using `by <field>`.

#### 2. Why an Analyst Uses It
Security incidents unfold over time. `timechart` shows when activity spikes, drops off, or clusters into specific hours—making it essential for timeline reconstruction and dashboard trend panels.

#### 3. Basic Syntax
```spl
... | timechart [span=<interval>] <agg_function>(<field>) [by <split_field>]
```

#### 4. Example
```spl
index=cybersecurity_lab
| timechart span=1h count by event.outcome
```

#### 5. Common Mistake
Omitting an explicit `span` (such as `span=1h` or `span=15m`) or misreading a timechart as proof of an attack—remembering that `span` controls bucket granularity (where `1h` can smooth out short bursts) and that a timechart alone shows *when* volume changed, not *why*.

#### 6. Practical SOC Use Case
In my dashboard and timeline checks, I use `timechart span=1h count` and `timechart span=1h count by event.outcome` to see whether failures, successes, blocks, or alerts cluster into a specific hour and then drill into the raw events from that window.

---

### 11. `fieldsummary`

#### 1. What It Does
`fieldsummary` generates a summary table describing the fields present in the current search results—including field names, data types, distinct value counts, numeric/min/max stats where applicable, and how many events contain each field.

#### 2. Why an Analyst Uses It
When you first ingest a dataset or inherit unfamiliar logs, `fieldsummary` gives you an instant map of what fields exist, which ones are actually populated, and what values they hold—without guessing.

#### 3. Basic Syntax
```spl
... | fieldsummary
```

#### 4. Example
```spl
index=cybersecurity_lab | fieldsummary
```

#### 5. Common Mistake
Running `| fieldsummary` over a massive, unfiltered dataset without scoping the index or time range first—which can be slow and overwhelming—or treating a field's presence in `fieldsummary` as proof that every event in the index has that field populated.

#### 6. Practical SOC Use Case
Right after loading my normalized Day 21 dataset into `cybersecurity_lab`, I run `index=cybersecurity_lab | fieldsummary` to verify which normalized fields were extracted, spot naming differences from sample snippets, and confirm which fields are present across the events.

---

## 5. What I Document & Remember as I Grow Toward Big Tech

* **Document Real Schema & Query Behavior:** Record actual field names, quirks (like `"event.category{}"`), and any data gaps in `docs/` and `reports/` so every query in the repository is reproducible.
* **Keep Pipelines Readable & Intentional:** Filter early, avoid unnecessary complexity, and pick the right command for the job (`stats` vs. `dedup`, `where` vs. `search`, `timechart` with explicit `span`).
* **Build Analyst Judgment Alongside Syntax:** Knowing SPL commands gets a query to run; knowing what a result *means*—and what it *doesn't* prove—is what makes you effective in a real SOC and in technical interviews.