# Technical Note: Multi-Source Telemetry Mapping, Schema Convergence & Raw Lineage Preservation

**Author:** Serah Mulwa

**Module:** Day 21 - SIEM Architecture, Log Ingestion & Security Data Engineering

## 1. Executive Summary & Personal Reflections

When building introductory cybersecurity projects, it is easy to work with a single, neatly formatted log file. However, real-world enterprise security operations are messy. A Security Operations Center receives telemetry from dozens of different security vendors, network sensors, and operating systems—each speaking a completely different dialect.

Windows domain controllers talk in Event IDs (`4625`, `4624`), network firewalls output connection blocks and allows, Suricata sends JSON intrusion detection alerts, and Zeek network monitors utilize epoch timestamps and connection flow IDs (`id.orig_h`, `id.resp_h`).

Without a rigorous normalisation and mapping protocol, security analysts would have to learn a dozen different syntaxes to investigate a single cyber attack. This technical note outlines the 6-step engineering protocol I implemented and tested in my Parrot OS lab environment to converge heterogeneous log sources into a unified Elastic Common Schema (ECS) subset while preserving complete forensic raw lineage.

## 2. The Multi-Source Integration Challenge & Lab Execution

In an advanced persistent threat (APT) campaign, an adversary never triggers just one log source. To validate this in my Mini-SIEM project (`day21-mini-siem`), I ingested four distinct synthetic log streams (`windows.jsonl`, `linux.jsonl`, `firewall.jsonl`, `suricata.jsonl`) generated in `data/raw/` (as evidenced in my terminal setup screenshots).

As captured in my pipeline execution screenshots (`day21-11-pipeline-execution-summary.png`), when running `python3 src/ingest.py`, the pipeline successfully processed these multi-source inputs, receiving 12 records, validating 9, isolating 3 malformed/invalid records into quarantine, catching 1 duplicate, and writing 8 normalized events.

## 3. The 6-Step Multi-Source Engineering Protocol

When onboarding a new log source into my Python Mini-SIEM ingestion pipeline (`src/ingest.py`), I followed a strict 6-step engineering protocol, backed by unit test verification (`day21-13-unit-test-results.png`):

### Step 1: Identify the Source Schema

Before writing parsing logic, I inspected raw log samples using terminal commands like `head -n 1 data/raw/windows.jsonl` (documented in `day21-07-raw-windows-sample.png`). This confirmed unique vendor field structures—for example, Windows utilizes `source_ip` and `username`, whereas firewall logs utilize `action` (`blocked`/`allowed`) and `destination_port`.

### Step 2: Select a Defensible Subset

Instead of attempting to parse every single field on day one, I focused on six core investigative anchors required for security triage:
* **Timestamp** (`@timestamp`)
* **Source IP** (`source.ip`)
* **Destination IP** (`destination.ip`)
* **User / Actor** (`user.name`)
* **Event Action** (`event.action`)
* **Event Outcome** (`event.outcome`)

### Step 3: Write Normalisation Mapping Logic

As shown in my code implementation screenshots (`day21-08-multi-source-normalizer.png` and `day21-09-raw-lineage-and-tests.png`), I implemented conditional Python mapping logic inside `normalise_record()` that safely extracts and translates source-specific keys into our unified ECS subset:

```python
# Extract source-specific IP fields safely across different log dialects
src_ip = record.get("source_ip") or record.get("id.orig_h") or record.get("src_ip")
dst_ip = record.get("destination_ip") or record.get("id.resp_h")

# Map source-specific actions into unified ECS actions
action = "unknown"
if source_name == "windows":
    event_id = record.get("event_id")
    action = "authentication_failure" if event_id == 4625 else "authentication_success"
elif source_name == "firewall":
    raw_action = record.get("action", "")
    action = f"network_connection_{raw_action}"
```

### Step 4: Preserve Raw Lineage (`raw_reference`)

Normalisation is essential for cross-tool searchability, but it abstracts away niche vendor details. As verified in my processed event inspection screenshots (`day21-06-processed-events-and-quarantine.png`), my pipeline attaches the complete original record dictionary to a `raw_reference` field (`normalized["raw_reference"] = record`). This ensures full forensic depth is retained alongside normalized events.

### Step 5: Test the Mapping with Unit Tests

To ensure code reliability, I added dedicated unit test methods inside `tests/test_ingest.py` covering Windows and Firewall normalization. Running `python3 -m unittest discover -s tests -v` confirmed a 100% passing test suite (`Ran 2 tests in 0.002s ... OK`, as captured in `day21-13-unit-test-results.png`).

## 4. Summary Schema Mapping Reference Table

| Investigative Anchor | ECS Target Field | Windows Source Key | Firewall Source Key | Zeek / Suricata Source Key | 
| ----- | ----- | ----- | ----- | ----- | 
| **Event Time** | `@timestamp` | `timestamp` | `timestamp` | `ts` | 
| **Source IP** | `source.ip` | `source_ip` | `source_ip` | `id.orig_h` | 
| **Destination IP** | `destination.ip` | `destination_ip` | `destination_ip` | `id.resp_h` | 
| **Actor / User** | `user.name` | `username` | N/A | `username` | 
| **Event Action** | `event.action` | `event_id` (4625/4624) | `action` (blocked/allowed) | `event_type` (alert) | 
| **Raw Lineage** | `raw_reference` | Complete original dict | Complete original dict | Complete original dict | 

## 5. Job Market Positioning

In Big Tech security engineering interviews (Microsoft, AWS, Google, Datadog), candidates are frequently evaluated on data onboarding scalability. Being able to articulate how you handle multi-source log normalization while maintaining forensic raw lineage—backed by terminal execution evidence and passing unit tests—proves that you design production-grade systems with both operational searchability and investigative depth in mind.
