# Day 23 — Part 2: What Is Sigma?

## Shifting Gears: From Searching Logs to Engineering Portable Detections

Coming out of Day 21 and Day 22, I feel like I am finally seeing how the pieces of a real security operations pipeline connect. On Day 21, the focus was getting security data collected, prepared, and brought into a SIEM cleanly. On Day 22, I spent time inside Splunk using SPL to search events, check field extractions, measure ingestion lag, and summarize activity like failed logons.

Today, on Day 23, the focus shifts to **detection engineering**—specifically designing security detections using **Sigma**. Instead of writing a query purely to explore logs in one tool right now, I am learning how to express detection logic in a structured, portable way that can be maintained like code and translated for different platforms.

---

## 2.1 The Problem Sigma Solves

### Why Platform-Specific Queries Create Friction

When you work in a single SIEM—say Splunk—it is very natural to write a search directly in **SPL (Search Processing Language)**. For example, to look for Windows failed logon events (Event ID `4625`), you might write:

```spl
index=security
EventCode=4625
```

That works well *if* you are in Splunk, *if* the data is in that `security` index, and *if* `EventCode` is populated and extracted the way you expect.

The trouble starts when you step outside a single tool or team. Imagine another organization—or another team inside a larger enterprise—uses **Microsoft Sentinel**, which relies on **Kusto Query Language (KQL)**, or **Elasticsearch**, which uses its own query syntax and schemas. You cannot just take a raw Splunk SPL string, drop it into Sentinel, and expect it to run cleanly.

When security teams write detections only in one SIEM's native query language, a few practical headaches show up:

* **Detections get locked to one platform:** Reusing that exact logic in another SIEM usually means rewriting it by hand.
* **Maintenance becomes harder:** If you update how you detect a behavior in one place, other copies in different tools can easily fall behind or drift.
* **Sharing and collaboration slow down:** Sharing detection ideas across teams, vendors, or open-source communities is much smoother when the logic is not tied to one proprietary query dialect.

### How Sigma Approaches the Problem

**Sigma** is an open, vendor-neutral format written in **YAML** for describing log-based detection rules. Rather than writing the final platform query by hand for every SIEM, you define the detection logic in a standardized YAML rule, and a conversion tool—such as **pySigma** (and CLI tooling built around it)—translates that rule into a query for a target backend (like Splunk SPL or another SIEM).

Here is how I visualize that flow right now:

```text
        SECURITY DATA
              |
              v
       DETECTION IDEA
              |
              v
       SIGMA RULE (YAML)
              |
              v
       pySigma ENGINE
              |
       +------+------+
       |             |
       v             v
    SPLUNK          OTHER
      SPL           SIEM
       |             |
       v             v
   INVESTIGATION   INVESTIGATION
```

The main benefit here is **portability**: you can keep one clear detection definition in version control and translate it for different security platforms instead of starting from scratch each time.

### Why Portability Is Not "Magic" (Important Realities)

One thing I want to be careful not to misunderstand is that Sigma does **not** make every detection work automatically everywhere. Even with a great rule and `pySigma`, real environments differ in ways that affect results:

* **Field names:** One log source or data model might use `EventCode`, another might use `event.code` or `WinEvent_ID`, or nest JSON fields in ways that need adjustment.
* **Log formats:** Raw logs, JSON events, and structured Windows/Linux/cloud logs do not all look the same.
* **Data models & normalization:** Whether fields are normalized at ingest or at search time makes a big difference.
* **Query capabilities & search semantics:** Different SIEMs handle wildcards, case sensitivity, regexes, aggregations, and time evaluation differently.
* **Backend pipelines:** A Sigma rule often needs a backend or processing pipeline tailored to how the target platform expects fields and logsources to be mapped.

To me, that is a really important lesson: **Sigma improves portability, but it never replaces understanding your actual telemetry.**

---

## 2.2 Sigma Versus SPL

Drawing a sharp line between **Sigma** and **SPL** helps me avoid mixing up *defining* a detection with *running* a search in Splunk.

| Feature | Sigma | Splunk SPL |
| :--- | :--- | :--- |
| **Purpose** | Describe portable, structured detection logic | Search, filter, transform, and analyze data inside Splunk |
| **Format** | YAML | Splunk Search Processing Language |
| **Platform dependency** | Designed to be vendor-neutral | Splunk-specific |
| **Main use** | Detection engineering, rule sharing, Detection-as-Code | Investigation, threat hunting, dashboards, and analytics |
| **Conversion** | Can be converted into supported backend queries (e.g., via `pySigma`) | Already a Splunk search query |
| **Portability** | Relatively high, subject to backend and field compatibility | Limited to compatible Splunk environments |

### Thinking of Sigma as the Blueprint and SPL as an Implementation

A simple way to keep them straight: **Sigma is the detection specification (the blueprint), and SPL is one possible implementation (a query built for Splunk).**

For example:

1. **Detection idea / Sigma specification:** Describe a rule that looks for Windows security events representing failed logons.
2. **Conversion:** Run the Sigma rule through a conversion backend to generate Splunk SPL.
3. **Execution & investigation:** Run that generated SPL inside Splunk to inspect matching events, pivot to related fields, and investigate what happened.

In my own workflow, I see Sigma as the place where I write down *what* behavior I want to catch and *why*, while SPL is what I run inside Splunk to search data, verify behavior, and dig deeper during an investigation.

---

## How to Practice This, Why It Matters for Careers, and What to Document

### How I Can Practice Part 2 Step by Step

1. **Pick a straightforward event type:** Start with something concrete like Windows failed logons or a single suspicious command-line pattern.
2. **Write the logic in plain English first:** State what event occurs, what log source should contain it, and what normal activity might look similar.
3. **Separate intent from syntax:** Look at a query and ask which parts are *what we are looking for* versus *how Splunk writes it*.
4. **Check field assumptions against real sample data:** Before trusting any field name in a converted query, check what fields actually exist in the test events.

### How This Applies in the Job Market (SOC & Detection Engineering)

In interviews for SOC analyst, detection engineer, or security engineering roles—including global and larger tech teams—hiring managers care a lot about **how you think about detections and data**:

* **Avoiding tool lock-in:** Teams that manage multiple platforms or migrate SIEMs value engineers who write portable detections rather than one-off queries locked inside a single console.
* **Understanding telemetry limits:** Knowing *why* a portable rule can still fail when field mappings or log sources do not match shows practical troubleshooting instincts instead of blind trust in tooling.
* **Detection-as-Code habits:** Storing rules cleanly, explaining intent clearly, and testing against sample data mirrors how modern security engineering teams work.

### What to Document & What I Must Remember

* **What to document in my Day 23 notes:**
  * My own explanation of the problem Sigma solves and the end-to-end flow from security data and detection idea to YAML rule, `pySigma` conversion, backend query, and investigation.
  * The comparison between **Sigma** and **SPL** along with a clear example (such as Windows failed logons).
  * The practical limits of portability (field names, log formats, data models, query capabilities, search semantics, and normalization).
* **What I must remember:**
  * Sigma is a **vendor-neutral detection format**, not a SIEM that runs rules by itself.
  * **SPL is for searching and analyzing in Splunk**; Sigma is for describing portable detection logic.
  * **Portability does not remove the need to know your logs**—field names, normalization, and telemetry coverage still decide whether a detection works in practice.