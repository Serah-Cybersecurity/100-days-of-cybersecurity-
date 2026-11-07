#!/usr/bin/env python3
"""
Day 21 — SIEM Architecture & Data Ingestion Pipeline
Mini-SIEM Log Ingestion, Validation, Normalisation, and Quality Reporting Engine

Accepts multi-source security telemetry (Suricata EVE JSON, Windows event samples, 
Syslog), validates schema integrity, isolates malformed records, normalises fields 
to an educational ECS subset, and outputs structured ingestion metrics.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_timestamp(ts_raw):
    """Normalises diverse timestamp formats into ISO-8601 UTC strings."""
    if not ts_raw:
        return datetime.now(timezone.utc).isoformat()
    
    # If already a float (epoch)
    if isinstance(ts_raw, (int, float)):
        try:
            return datetime.fromtimestamp(float(ts_raw), tz=timezone.utc).isoformat()
        except (ValueError, OverflowError):
            pass

    ts_str = str(ts_raw).strip()
    # Try ISO parsing
    try:
        clean_str = ts_str.replace("+0000", "+00:00")
        dt = datetime.fromisoformat(clean_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except ValueError:
        pass

    return datetime.now(timezone.utc).isoformat()


def normalise_record(raw_record):
    """
    Normalises raw heterogeneous telemetry records into an ECS subset:
      - @timestamp
      - event.dataset (source type)
      - event.action / event.kind
      - source.ip, source.port
      - destination.ip, destination.port
      - network.transport / protocol
      - observer.vendor
    """
    normalized = {
        "@timestamp": parse_timestamp(raw_record.get("timestamp") or raw_record.get("ts")),
        "event": {
            "dataset": raw_record.get("event_type") or raw_record.get("log_source", "unknown"),
            "kind": raw_record.get("event_kind", "alert" if "alert" in raw_record else "event")
        },
        "source": {
            "ip": raw_record.get("src_ip") or raw_record.get("id.orig_h") or raw_record.get("source_ip"),
            "port": raw_record.get("src_port") or raw_record.get("id.orig_p") or raw_record.get("source_port")
        },
        "destination": {
            "ip": raw_record.get("dest_ip") or raw_record.get("id.resp_h") or raw_record.get("destination_ip"),
            "port": raw_record.get("dest_port") or raw_record.get("id.resp_p") or raw_record.get("destination_port")
        },
        "network": {
            "transport": str(raw_record.get("proto") or raw_record.get("protocol", "")).lower()
        },
        "observer": {
            "vendor": raw_record.get("vendor", "Suricata/Zeek/Syslog Simulator")
        },
        "raw_reference": raw_record  # Preserve original event for lineage
    }
    return normalized


def run_pipeline(input_path, output_dir):
    input_file = Path(input_path)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    normalized_out = out_path / "normalized_events.jsonl"
    quarantine_out = out_path / "quarantine_malformed.jsonl"

    total_lines = 0
    valid_records = 0
    malformed_records = 0
    duplicate_records = 0
    seen_hashes = set()

    print("==========================================================")
    print("      DAY 21: SIEM INGESTION & NORMALISATION PIPELINE     ")
    print("==========================================================")
    print(f"[*] Processing input telemetry: {input_file}")

    if not input_file.exists():
        print(f"[-] Error: Input file {input_file} not found.")
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8") as fin, \
         open(normalized_out, "w", encoding="utf-8") as f_norm, \
         open(quarantine_out, "w", encoding="utf-8") as f_quar:

        for line_num, line in enumerate(fin, start=1):
            line_str = line.strip()
            if not line_str:
                continue
            total_lines += 1

            # 1. Syntax Validation (JSON Parsing)
            try:
                record = json.loads(line_str)
            except json.JSONDecodeError as err:
                malformed_records += 1
                quarantine_entry = {
                    "line_number": line_num,
                    "error": str(err),
                    "raw_content": line_str,
                    "quarantine_timestamp": datetime.now(timezone.utc).isoformat()
                }
                f_quar.write(json.dumps(quarantine_entry) + "\n")
                continue

            # 2. Schema Validation (Required Field Checks)
            # Must have at least a timestamp equivalent or source identifier
            if not any(k in record for k in ["timestamp", "ts", "src_ip", "id.orig_h", "message"]):
                malformed_records += 1
                quarantine_entry = {
                    "line_number": line_num,
                    "error": "Missing mandatory telemetry anchor fields",
                    "raw_content": record,
                    "quarantine_timestamp": datetime.now(timezone.utc).isoformat()
                }
                f_quar.write(json.dumps(quarantine_entry) + "\n")
                continue

            # 3. Deduplication Check (using JSON string hash)
            record_hash = hash(line_str)
            if record_hash in seen_hashes:
                duplicate_records += 1
                continue
            seen_hashes.add(record_hash)

            # 4. Normalisation Step (ECS mapping)
            norm_event = normalise_record(record)
            f_norm.write(json.dumps(norm_event) + "\n")
            valid_records += 1

    # 5. Generate Ingestion Metrics Report
    print("----------------------------------------------------------")
    print(f"[+] Total Lines Scanned        : {total_lines}")
    print(f"[+] Valid Normalised Events    : {valid_records}")
    print(f"[-] Malformed / Quarantined    : {malformed_records}")
    print(f"[-] Duplicate Events Dropped   : {duplicate_records}")
    print(f"[*] Normalised Output File     : {normalized_out}")
    print(f"[*] Quarantine Output File     : {quarantine_out}")
    print("==========================================================")

    # Write summary statistics report
    report_path = out_path / "ingestion-metrics.json"
    metrics = {
        "execution_timestamp": datetime.now(timezone.utc).isoformat(),
        "total_lines_processed": total_lines,
        "valid_records": valid_records,
        "malformed_records": malformed_records,
        "duplicate_records": duplicate_records,
        "ingestion_success_rate": (valid_records / total_lines * 100) if total_lines > 0 else 0
    }
    with open(report_path, "w", encoding="utf-8") as freport:
        json.dump(metrics, freport, indent=2)
    print(f"[+] Ingestion report saved to  : {report_path}")


def main():
    parser = argparse.ArgumentParser(description="Day 21 Mini-SIEM Ingestion Pipeline")
    parser.add_argument("--input", default="input/sample_security_logs.jsonl", help="Path to raw log file")
    parser.add_argument("--output-dir", default="output", help="Directory for pipeline output")

    args = parser.parse_args()
    run_pipeline(args.input, args.output_dir)


if __name__ == "__main__":
    main()
