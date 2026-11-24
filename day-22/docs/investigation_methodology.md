# Investigation Methodology — Splunk Security Workbench

**Author:** Serah Kathini Mulwa

**Program:** Women Techsters Fellowship — Cybersecurity Track

**Project:** Day 22 — Splunk Fundamentals & Search Processing Language (SPL)

**Target Index:** `cybersecurity_lab` (`sourcetype="_json"`)

## 1. Why I Follow a Structured Investigation Methodology

When I first started looking at security logs, it was tempting to jump straight into writing clever queries and calling every spike or failed login an attack. Working through this Day 22 Splunk workbench showed me how quickly that mindset can lead to false alarms, missed context, or wasted time.

A repeatable investigation methodology keeps my analysis grounded in actual evidence. Rather than treating every anomaly as proof of compromise, I follow a consistent sequence:

1. **Preserve evidence and verify reproducibility** before touching any search bar.
2. **Inspect the real schema and field extraction** instead of guessing field names from examples.
3. **Scope early, inspect raw events, and aggregate thoughtfully** using SPL pipes.
4. **Separate raw observations from analytical conclusions** so every finding stays honest and defensible.
5. **Distinguish ad-hoc searching from detection engineering** before thinking about automated alerting.

## 2. Step-by-Step Investigation Workflow

### Step 1: Evidence Preservation & Environment Scoping

Before running any searches, I keep my Day 21 Python Mini-SIEM project intact and copy `normalised_events.jsonl` into `data/source/normalised_events.jsonl` inside the Day 22 repository without altering the source data. Inside Splunk, I isolate my lab work in a dedicated index (`cybersecurity_lab`) with `sourcetype="_json"` so training events stay separate from default or internal logs.

When troubleshooting zero-result searches, I check the basics systematically before assuming my query logic is broken:

* Did the upload and indexing job finish cleanly?
* Am I querying `index=cybersecurity_lab`?
* Is the time range set appropriately (such as **All time** for static lab datasets)?
* Were timestamps parsed cleanly, and are there any parsing or line-breaking issues?

### Step 2: Schema & Field Discovery First

One of the most important habits I built on Day 22 is **never assuming a field exists or behaves a certain way just because it appears in a sample snippet**.

In my `normalised_events.jsonl` dataset, testing real queries showed me practical details about how fields appear in Splunk:

* Nested JSON array fields such as `event.category` extract with curly braces (`"event.category{}"`), so filtering on `"event.category{}"` matches array values reliably.
* Some expected fields—such as DNS query fields (`dns.question.name`)—are not present in every event or in this small sample batch, while other fields (such as `host.name`) can be `null` on certain sensor events like Suricata alerts.
* Grouping with `stats count by fieldA, fieldB, fieldC` only retains events where all listed fields exist on that record, so I keep multi-field groupings tailored to the event subset I am inspecting.

### Step 3: SPL Pipeline Discipline ("Filter Early, Aggregate Late")

Because SPL evaluates commands sequentially from left to right across pipes (`|`), query order matters:

* **Filter early:** Put `index=cybersecurity_lab`, time ranges, and key event filters up front so Splunk narrows the candidate event set quickly and preserves event-level fields before summarizing.
* **Inspect raw and tabular context:** Use `head`, `table`, and field inspection to see actual timestamps, users, IPs, ports, actions, and outcomes before drawing conclusions.
* **Aggregate late:** Use `stats`, `dc()`, and `timechart` once you know what you are counting and why.

When using `timechart`, I always explicitly specify a `span` (such as `span=1h` or `span=15m`) so time buckets stay predictable and easy to compare across searches and dashboard panels.

### Step 4: Five-Area SOC Triage Framework

During my Day 22 analysis of `cybersecurity_lab`, I organized my investigation around five core operational areas:

1. **Authentication Activity:** Baseline total authentication records, compare `success` vs. `failure` counts, and review which accounts and hosts appear.
2. **Failed Authentication Sources:** Rank originating IPs (`source.ip`) by failed attempts and pair counts with distinct targeted accounts (`dc(user.name)`) to see whether activity looks like single-account retries/brute force or broader spraying/scanning.
3. **DNS & Network Detection Telemetry:** Check for DNS query fields and response patterns where available, and review network detection events (such as Suricata `intrusion_detection_alert` records) alongside surrounding context.
4. **Firewall & Connection Activity:** Review source/destination IPs, destination ports, and allowed vs. blocked actions (`network_connection_allowed`, `network_connection_blocked`) to understand perimeter behavior.
5. **Time-Based Analysis:** Use `timechart` with explicit spans to spot clustering, sudden shifts in volume, or off-hours patterns—always treating the chart as a starting point to inspect underlying events rather than standalone proof.

## 3. Separating Observations from Conclusions

A core rule in my reporting (`reports/investigation_report.md` and `dashboards/dashboard_design.md`) is keeping **what I observed** separate from **what I suspect or need to verify next**:

* **A failed login is not automatically an attack:** It can come from a mistyped password, expired credentials, a cached token, a scheduled script, or a misconfigured service just as easily as from credential guessing.
* **A high failure count or network anomaly is a lead, not proof:** Seeing failed logins from an IP, a blocked outbound connection, or an IDS alert tells me where to look closer—not that compromise has already occurred.
* **Context closes the gap:** To move from a lead to a solid conclusion in a real environment, I look for supporting context such as whether a login later succeeded from that source, what host or account is involved, whether NAT/proxies/scanners explain the traffic, and what additional logs (like identity provider logs, endpoint telemetry, or packet/flow details) are needed.

## 4. Searching vs. Detection Engineering Mindset

Developing strong search skills is essential for threat hunting and incident investigation, but **running a search is not the same thing as engineering a production detection**:

* **A search** is a query I run to explore data, answer a question, or test a hypothesis on demand.
* **A detection** is a structured, repeatable analytic designed to identify activity that warrants investigation in a reliable, manageable way.

For example, running:

```spl
index=cybersecurity_lab "event.category{}"="authentication" event.outcome="failure"
| stats count by source.ip
```

shows failed authentication counts by source IP in the dataset—that is a search. Thinking about a detection concept—such as spotting a source IP generating a high number of failed authentication events within a defined time window—is only the starting point.

Before promoting any hunt idea into a real production alert (which I will explore further on Day 23 with Sigma), an engineer has to account for practical operational factors:

* **Data coverage:** Are the right log sources collected across the environment without blind spots?
* **Event quality:** Are timestamps accurate and required fields normalized and populated reliably?
* **Time windows:** What time window actually fits the behavior (for example, short bursts vs. longer windows)?
* **Expected baselines:** What looks normal for this environment?
* **Legitimate operational activity:** What routine admin tasks, scanners, service accounts, or user mistakes could trigger noise?
* **Alert severity:** How serious is the risk if the condition is real?
* **False-positive rates:** How much noise will analysts have to wade through?
* **Suppression and grouping:** How should repeated matching events be grouped or throttled so analysts aren't flooded?
* **Investigation steps:** What should the investigating analyst check first when it triggers?
* **Escalation criteria:** When should an alert be escalated versus closed?

For Day 22, my focus stays on disciplined investigation, clear documentation, and honest analysis rather than rushing half-tuned alerts into production.

## 5. Key Takeaways I Keep in Mind

1. **Inspect before assuming:** Always check actual fields, array syntax (`"event.category{}"`), and time ranges against real data.
2. **Filter early, aggregate late, and set `span`:** Keep SPL pipelines clean and time charts consistent.
3. **Leads are not proof:** Separate raw facts from assumptions, and always state limitations clearly.
4. **Searching is step one; detection engineering is a bigger discipline:** Master investigation first, then build on it with Sigma on Day 23.