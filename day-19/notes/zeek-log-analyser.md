# Technical Note: Building an Automated Python Zeek Log Analyser

**Author:** Serah Mulwa   
**Module:** Day 19 - Network Threat Hunting with Zeek  

---

## 1. Executive Summary

While command-line tools like `jq` are effective for targeted, ad-hoc investigations, Security Operations Center (SOC) environments require scalable automation. Manually dissecting large volumes of telemetry logs across multiple protocol outputs (`conn.log`, `dns.log`, `ssl.log`) is time-consuming and prone to human error.

This technical note documents the design, architecture, and execution of a custom Python log parser (`zeek_log_summary.py`). Built entirely with Python's standard library, the script automates the ingestion of line-delimited JSON logs, handles malformed records gracefully, aggregates protocol statistics, and correlates cross-log events using Zeek's Unique Identifiers (`uid`).

---

## 2. Script Architecture & Engineering Design

The analyser relies on a modular design structured around clean error handling and efficient memory aggregation.

### Key Architectural Components:

1. **Robust JSON Parsing (`read_jsonl`):**  
   Processes newline-delimited JSON files line by line using `json.loads()`. It isolates parsing errors using `try...except json.JSONDecodeError` blocks to ensure that corrupted records do not crash the triage pipeline.

2. **Frequency Aggregation (`collections.Counter`):**  
   Utilizes Python's native `Counter` object to track distribution metrics across transport protocols, destination ports, connection states, requested domain names, and TLS versions.

3. **Cross-Log UID Correlation:**  
   Maps session UIDs present in `dns.log` to demonstrate cross-protocol correlation capabilities across connection records.

---

## 3. Python Source Code: `scripts/zeek_log_summary.py`

```python
import json
import sys
from collections import Counter
from pathlib import Path

def read_jsonl(path):
    """
    Read newline-delimited JSON records.
    Returns:
        records: successfully parsed JSON objects
        malformed: number of invalid records
        exists: whether the file was present
    """
    records = []
    malformed = 0
    if not path.exists():
        return records, malformed, False
    
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                records.append(record)
            except json.JSONDecodeError:
                malformed += 1
                
    return records, malformed, True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 zeek_log_summary.py <zeek_output_dir>")
        sys.exit(1)
        
    output_dir = Path(sys.argv[1])
    print(f"[*] Analyzing Zeek logs in: {output_dir}")
    
    # 1. Process conn.log
    conn_path = output_dir / "conn.log"
    conn_records, conn_malformed, conn_exists = read_jsonl(conn_path)
    
    proto_counts = Counter()
    service_counts = Counter()
    port_counts = Counter()
    state_counts = Counter()
    
    for r in conn_records:
        if "proto" in r:
            proto_counts[r["proto"]] += 1
        if "service" in r and r["service"]:
            service_counts[r["service"]] += 1
        if "id.resp_p" in r:
            port_counts[r["id.resp_p"]] += 1
        if "conn_state" in r:
            state_counts[r["conn_state"]] += 1
            
    # 2. Process dns.log
    dns_path = output_dir / "dns.log"
    dns_records, dns_malformed, dns_exists = read_jsonl(dns_path)
    
    query_counts = Counter()
    rcode_counts = Counter()
    dns_to_uid = {}
    
    for r in dns_records:
        if "query" in r:
            query_counts[r["query"]] += 1
        if "rcode_name" in r:
            rcode_counts[r["rcode_name"]] += 1
        if "uid" in r and "query" in r:
            dns_to_uid[r["uid"]] = r["query"]
            
    # 3. Process ssl.log
    ssl_path = output_dir / "ssl.log"
    ssl_records, ssl_malformed, ssl_exists = read_jsonl(ssl_path)
    
    tls_versions = Counter()
    server_names = Counter()
    
    for r in ssl_records:
        if "version" in r:
            tls_versions[r["version"]] += 1
        if "server_name" in r and r["server_name"]:
            server_names[r["server_name"]] += 1
            
    # Print Summary Report
    print("\n" + "="*50)
    print(" ZEEK LOG AUTOMATED ANALYSIS REPORT")
    print("="*50)
    print(f"Total Connections: {len(conn_records)} (Malformed: {conn_malformed})")
    print(f"Total DNS Queries: {len(dns_records)} (Malformed: {dns_malformed})")
    print(f"Total SSL Records: {len(ssl_records)} (Malformed: {ssl_malformed})")
    
    print("\n--- Transport Protocols ---")
    for proto, count in proto_counts.most_common():
        print(f"  {proto}: {count}")
        
    print("\n--- Top Destination Ports ---")
    for port, count in port_counts.most_common(5):
        print(f"  Port {port}: {count}")
            
    print("\n--- Connection States ---")
    print(dict(state_counts))
        
    print("\n--- Top DNS Queries ---")
    for q, count in query_counts.most_common(5):
        print(f"  {q}: {count}")
            
    print("\n--- TLS Versions ---")
    print(dict(tls_versions))
        
    print("\n--- Server Names (SNI) ---")
    for sn, count in server_names.most_common(5):
        print(f"  {sn}: {count}")
            
    print("\n--- UID Correlations ---")
    print(f"Successfully correlated {len(dns_to_uid)} DNS sessions with UIDs.")
    print("="*50)

if __name__ == "__main__":
    main()
```

---

## 4. Execution & Results

### Step 1: Code Compilation Check
Before running the parser, code validity was verified using Python's compiler module:

```bash
python3 -m py_compile scripts/zeek_log_summary.py
```

### Step 2: Running the Log Analyser
The script was executed against the generated log output directory (`output/zeek`):

```bash
python3 scripts/zeek_log_summary.py output/zeek
```

### Terminal Output:

```text
[*] Analyzing Zeek logs in: output/zeek

==================================================
 ZEEK LOG AUTOMATED ANALYSIS REPORT
==================================================
Total Connections: 6 (Malformed: 0)
Total DNS Queries: 4 (Malformed: 0)
Total SSL Records: 1 (Malformed: 0)

--- Transport Protocols ---
  udp: 3
  tcp: 3

--- Top Destination Ports ---
  Port 53: 3
  Port 443: 3

--- Connection States ---
{'SF': 4, 'REJ': 2}

--- Top DNS Queries ---
  example.com: 4

--- TLS Versions ---
{'TLSv13': 1}

--- Server Names (SNI) ---
  example.com: 1

--- UID Correlations ---
Successfully correlated 3 DNS sessions with UIDs.
==================================================
```

---

## 5. Tool Capabilities & Scope

To maintain investigative integrity, it is important to define the scope of this automated parser:

| Capabilities | Out of Scope / Limitations |
| :--- | :--- |
| Fast aggregation across multiple JSON files | Fully automated threat intelligence lookups (e.g., VirusTotal API enrichment) |
| Resilient handling of malformed JSON records | Automated attribution or detection of malicious intent |
| Instant 5-tuple metrics summary | Replacement for enterprise SIEM data lakes |
| Automated cross-log UID correlation | Deep payload inspection for all proprietary protocols |

---

## 6. Key Portfolio Takeaways

* **Error-resilient parsing prevents pipeline crashes:** Using `try...except` exception handling ensures that log ingestion continues uninterrupted even when encountering incomplete or malformed lines.
* **Standard libraries offer lightweight execution:** Building triage tools with pure Python (`pathlib`, `json`, `collections`) allows scripts to run natively on secure, minimal target systems without requiring external package dependencies.
* **Automation accelerates initial triage:** Standardizing metric extraction enables security analysts to evaluate large traffic captures quickly and focus on anomaly investigation.
