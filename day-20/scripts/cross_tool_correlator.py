#!/usr/bin/env python3
"""
Day 20 — Integrated Network Threat Hunting & Detection Engineering
Cross-Tool Correlation Engine (Suricata EVE JSON + Zeek Logs)

Correlates Suricata EVE JSON alerts with Zeek network logs using:
  1. Community ID flow hashing
  2. Transport protocol validation
  3. Bi-directional endpoint (IP/Port tuple) verification
  4. Configurable timestamp proximity windowing (--window-seconds)
  5. Zeek UID pivoting for DNS and TLS context enrichment
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def parse_iso8601(ts_str):
    """Parses ISO-8601 strings (Suricata timestamps) into epoch seconds."""
    if not ts_str:
        return None
    try:
        # Handle ISO format strings like '2026-11-06T10:43:12.149350+0000'
        ts_clean = ts_str.replace("+0000", "+00:00")
        dt = datetime.fromisoformat(ts_clean)
        return dt.timestamp()
    except ValueError:
        return None


def parse_zeek_ts(ts_val):
    """Parses float or string epoch seconds (Zeek timestamps)."""
    if ts_val is None:
        return None
    try:
        return float(ts_val)
    except (ValueError, TypeError):
        return None


def load_jsonl(path):
    """
    Loads newline-delimited JSON records from a file.
    Returns valid dictionary records and a count of malformed lines.
    """
    records = []
    malformed = 0
    if not path or not Path(path).exists():
        return records, malformed

    with Path(path).open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                records.append(record)
            except json.JSONDecodeError:
                malformed += 1

    return records, malformed


def endpoints_match(sur_src_ip, sur_src_p, sur_dst_ip, sur_dst_p,
                    zeek_src_ip, zeek_src_p, zeek_dst_ip, zeek_dst_p):
    """
    Validates endpoint pairs bi-directionally (Forward or Reverse flow).
    """
    forward = (
        sur_src_ip == zeek_src_ip and int(sur_src_p or 0) == int(zeek_src_p or 0) and
        sur_dst_ip == zeek_dst_ip and int(sur_dst_p or 0) == int(zeek_dst_p or 0)
    )
    reverse = (
        sur_src_ip == zeek_dst_ip and int(sur_src_p or 0) == int(zeek_dst_p or 0) and
        sur_dst_ip == zeek_src_ip and int(sur_dst_p or 0) == int(zeek_src_p or 0)
    )
    return forward or reverse


def correlate_logs(suricata_dir, zeek_dir, window_seconds):
    """Executes multi-factor correlation across Suricata and Zeek logs."""
    sur_path = Path(suricata_dir) / "eve.json"
    zeek_conn_path = Path(zeek_dir) / "conn.log"
    zeek_dns_path = Path(zeek_dir) / "dns.log"
    zeek_ssl_path = Path(zeek_dir) / "ssl.log"

    # 1. Load telemetry sources
    sur_records, sur_malformed = load_jsonl(sur_path)
    conn_records, conn_malformed = load_jsonl(zeek_conn_path)
    dns_records, dns_malformed = load_jsonl(zeek_dns_path)
    ssl_records, ssl_malformed = load_jsonl(zeek_ssl_path)

    # Filter Suricata alerts
    alerts = [r for r in sur_records if r.get("event_type") == "alert"]

    # Index Zeek conn.log by Community ID
    zeek_by_comm_id = defaultdict(list)
    for conn in conn_records:
        comm_id = conn.get("community_id")
        if comm_id:
            zeek_by_comm_id[comm_id].append(conn)

    # Index Zeek DNS and SSL records by Zeek UID
    dns_by_uid = defaultdict(list)
    for dns in dns_records:
        uid = dns.get("uid")
        if uid:
            dns_by_uid[uid].append(dns)

    ssl_by_uid = defaultdict(list)
    for ssl in ssl_records:
        uid = ssl.get("uid")
        if uid:
            ssl_by_uid[uid].append(ssl)

    # 2. Perform correlation and validation logic
    correlated_results = []
    validation_failures = 0

    for alert in alerts:
        comm_id = alert.get("community_id")
        alert_ts = parse_iso8601(alert.get("timestamp"))
        sur_proto = str(alert.get("proto", "")).upper()
        sur_src_ip = alert.get("src_ip")
        sur_src_p = alert.get("src_port")
        sur_dst_ip = alert.get("dest_ip")
        sur_dst_p = alert.get("dest_port")
        signature = alert.get("alert", {}).get("signature", "Unknown Signature")
        sid = alert.get("alert", {}).get("signature_id", 0)

        if not comm_id or comm_id not in zeek_by_comm_id:
            validation_failures += 1
            continue

        candidate_conns = zeek_by_comm_id[comm_id]
        matched_conn = None

        for conn in candidate_conns:
            zeek_proto = str(conn.get("proto", "")).upper()
            zeek_ts = parse_zeek_ts(conn.get("ts"))
            zeek_src_ip = conn.get("id.orig_h")
            zeek_src_p = conn.get("id.orig_p")
            zeek_dst_ip = conn.get("id.resp_h")
            zeek_dst_p = conn.get("id.resp_p")

            # Check 1: Transport Protocol Match
            if sur_proto != zeek_proto:
                continue

            # Check 2: Bi-directional Endpoint Match
            if not endpoints_match(sur_src_ip, sur_src_p, sur_dst_ip, sur_dst_p,
                                   zeek_src_ip, zeek_src_p, zeek_dst_ip, zeek_dst_p):
                continue

            # Check 3: Timestamp Window Proximity
            if alert_ts is not None and zeek_ts is not None:
                if abs(alert_ts - zeek_ts) > window_seconds:
                    continue

            matched_conn = conn
            break

        if matched_conn:
            uid = matched_conn.get("uid")
            associated_dns = dns_by_uid.get(uid, [])
            associated_ssl = ssl_by_uid.get(uid, [])

            correlated_results.append({
                "community_id": comm_id,
                "signature": signature,
                "sid": sid,
                "suricata_timestamp": alert.get("timestamp"),
                "zeek_uid": uid,
                "protocol": sur_proto,
                "source": f"{sur_src_ip}:{sur_src_p}",
                "destination": f"{sur_dst_ip}:{sur_dst_p}",
                "dns_records": associated_dns,
                "ssl_records": associated_ssl
            })
        else:
            validation_failures += 1

    # 3. Output Summary Report
    print("==========================================================")
    print("      DAY 20: INTEGRATED THREAT HUNTING CORRELATION REPORT ")
    print("==========================================================")
    print(f"[*] Suricata Total Records Parsed : {len(sur_records)} (Malformed: {sur_malformed})")
    print(f"[*] Suricata Alerts Identified    : {len(alerts)}")
    print(f"[*] Zeek Connection Records       : {len(conn_records)} (Malformed: {conn_malformed})")
    print(f"[*] Zeek DNS Records Loaded       : {len(dns_records)}")
    print(f"[*] Zeek TLS/SSL Records Loaded   : {len(ssl_records)}")
    print(f"[*] Configured Time Window        : {window_seconds} seconds")
    print("----------------------------------------------------------")
    print(f"[+] Successfully Correlated Matches : {len(correlated_results)}")
    print(f"[-] Validation / Correlation Failures: {validation_failures}")
    print("==========================================================\n")

    for idx, res in enumerate(correlated_results, start=1):
        print(f"--- MATCH RECORD #{idx} ---")
        print(f"  Community ID    : {res['community_id']}")
        print(f"  Alert Signature : [{res['sid']}] {res['signature']}")
        print(f"  Flow Tuple      : {res['source']} -> {res['destination']} ({res['protocol']})")
        print(f"  Zeek Session UID: {res['zeek_uid']}")
        if res['dns_records']:
            for dns in res['dns_records']:
                print(f"  └─ Associated DNS Query : {dns.get('query')} (Type: {dns.get('qtype_name')}) -> Answers: {dns.get('answers')}")
        if res['ssl_records']:
            for ssl in res['ssl_records']:
                print(f"  └─ Associated TLS Server: {ssl.get('server_name')}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Day 20 Cross-Tool Telemetry Correlator")
    parser.add_argument("--suricata-dir", default="output/suricata", help="Path to Suricata logs directory")
    parser.add_argument("--zeek-dir", default="output/zeek", help="Path to Zeek logs directory")
    parser.add_argument("--window-seconds", type=float, default=30.0, help="Max allowed timestamp delta (seconds)")

    args = parser.parse_args()
    correlate_logs(args.suricata-dir if hasattr(args, 'suricata-dir') else args.suricata_dir,
                   args.zeek-dir if hasattr(args, 'zeek-dir') else args.zeek_dir,
                   args.window_seconds)


if __name__ == "__main__":
    main()
