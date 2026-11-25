#!/usr/bin/env python3
"""
Day 16: Defensive DNS Traffic Analysis Utility.

Purpose:
    Analyse synthetic DNS telemetry and identify
    clients exhibiting multiple unusual indicators.

Scope:
    Offline analysis of supplied JSONL records.

Limitations:
    Heuristic analysis only.
    No domain is classified as malicious automatically.
"""

import argparse
import ipaddress
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

REQUIRED_FIELDS = {
    "timestamp",
    "client_ip",
    "query_name",
    "query_type",
    "response_code",
}

def parse_timestamp(value):
    if not isinstance(value, str):
        raise ValueError("Timestamp must be a string.")
    
    parsed = datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )
    
    if parsed.tzinfo is None:
        raise ValueError(
            "Timestamp must include timezone information."
        )
    
    return parsed.astimezone(timezone.utc)

def validate_query_name(value):
    if not isinstance(value, str):
        raise ValueError("Query name must be a string.")
    
    name = value.rstrip(".").lower()
    
    if not name:
        raise ValueError("Query name is empty.")
    
    if len(name) > 253:
        raise ValueError("Query name is too long.")
    
    labels = name.split(".")
    
    if any(not label for label in labels):
        raise ValueError("Query name contains an empty label.")
    
    if any(len(label) > 63 for label in labels):
        raise ValueError("A DNS label exceeds 63 characters.")
    
    return name

def load_events(path):
    events = []
    invalid_records = 0
    
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                if not raw_line.strip():
                    continue
                
                try:
                    event = json.loads(raw_line)
                    
                    if not isinstance(event, dict):
                        raise ValueError(
                            "Record must be a JSON object."
                        )
                    
                    missing = REQUIRED_FIELDS - event.keys()
                    
                    if missing:
                        raise ValueError(
                            f"Missing fields: {sorted(missing)}"
                        )
                    
                    event["_time"] = parse_timestamp(
                        event["timestamp"]
                    )
                    
                    event["client_ip"] = str(
                        ipaddress.ip_address(event["client_ip"])
                    )
                    
                    event["query_name"] = validate_query_name(
                        event["query_name"]
                    )
                    
                    event["query_type"] = str(
                        event["query_type"]
                    ).upper()
                    
                    event["response_code"] = str(
                        event["response_code"]
                    ).upper()
                    
                    events.append(event)
                
                except (
                    json.JSONDecodeError,
                    ValueError,
                    TypeError,
                ) as exc:
                    invalid_records += 1
                    print(
                        f"WARNING line {line_number}: {exc}",
                        file=sys.stderr,
                    )
    
    except OSError as exc:
        print(
            f"ERROR: Unable to read input file: {exc}",
            file=sys.stderr,
        )
        return None, invalid_records
    
    return events, invalid_records

def peak_queries(events, window_minutes):
    ordered = sorted(
        event["_time"] for event in events
    )
    
    window = timedelta(minutes=window_minutes)
    left = 0
    peak = 0
    
    for right, current_time in enumerate(ordered):
        while (
            current_time - ordered[left] > window
        ):
            left += 1
        
        count = right - left + 1
        peak = max(peak, count)
    
    return peak

def analyse_client(events, args):
    total = len(events)
    
    unique_names = len({
        event["query_name"] for event in events
    })
    
    txt_count = sum(
        event["query_type"] == "TXT"
        for event in events
    )
    
    nxdomain_count = sum(
        event["response_code"] == "NXDOMAIN"
        for event in events
    )
    
    max_name_length = max(
        len(event["query_name"])
        for event in events
    )
    
    txt_ratio = txt_count / total if total else 0
    nxdomain_ratio = (
        nxdomain_count / total if total else 0
    )
    
    peak = peak_queries(
        events,
        args.window_minutes,
    )
    
    indicators = []
    
    if peak >= args.min_queries:
        indicators.append("high query frequency")
    
    if max_name_length >= args.long_name:
        indicators.append("long query names")
    
    if (
        txt_count >= args.min_txt
        and txt_ratio >= args.txt_ratio
    ):
        indicators.append("high TXT-query proportion")
    
    if (
        nxdomain_count >= args.min_nxdomain
        and nxdomain_ratio >= args.nxdomain_ratio
    ):
        indicators.append("repeated NXDOMAIN responses")
    
    return {
        "total": total,
        "unique_names": unique_names,
        "txt_count": txt_count,
        "txt_ratio": txt_ratio,
        "nxdomain_count": nxdomain_count,
        "nxdomain_ratio": nxdomain_ratio,
        "max_name_length": max_name_length,
        "peak_queries": peak,
        "indicators": indicators,
    }

def main():
    parser = argparse.ArgumentParser(
        description="Analyse synthetic DNS telemetry."
    )
    
    parser.add_argument(
        "logfile",
        type=Path,
        help="Path to JSONL DNS telemetry."
    )
    
    parser.add_argument(
        "--window-minutes",
        type=int,
        default=10,
    )
    
    parser.add_argument(
        "--min-queries",
        type=int,
        default=8,
    )
    
    parser.add_argument(
        "--long-name",
        type=int,
        default=60,
    )
    
    parser.add_argument(
        "--min-txt",
        type=int,
        default=4,
    )
    
    parser.add_argument(
        "--txt-ratio",
        type=float,
        default=0.50,
    )
    
    parser.add_argument(
        "--min-nxdomain",
        type=int,
        default=3,
    )
    
    parser.add_argument(
        "--nxdomain-ratio",
        type=float,
        default=0.30,
    )
    
    args = parser.parse_args()
    
    if (
        args.window_minutes < 1
        or args.min_queries < 1
        or args.long_name < 1
        or args.min_txt < 1
        or not 0 <= args.txt_ratio <= 1
        or args.min_nxdomain < 1
        or not 0 <= args.nxdomain_ratio <= 1
    ):
        parser.error("Detection parameters are invalid.")
    
    events, invalid = load_events(args.logfile)
    
    if events is None:
        return 2
    
    if not events:
        print("ERROR: No valid DNS events were processed.")
        return 1
    
    grouped = defaultdict(list)
    
    for event in events:
        grouped[event["client_ip"]].append(event)
    
    print("\n===== DNS ANALYSIS SUMMARY =====")
    print(f"Valid records: {len(events)}")
    print(f"Invalid records: {invalid}")
    print(f"Unique clients: {len(grouped)}")
    
    print("\n===== CLIENT ANALYSIS =====")
    
    review_count = 0
    
    for client_ip, client_events in sorted(grouped.items()):
        result = analyse_client(client_events, args)
        
        print(f"\nClient: {client_ip}")
        print(f"Total queries: {result['total']}")
        print(f"Unique query names: {result['unique_names']}")
        print(f"Maximum query-name length: {result['max_name_length']}")
        print(f"TXT queries: {result['txt_count']} ({result['txt_ratio']:.0%})")
        print(f"NXDOMAIN responses: {result['nxdomain_count']}")
        print(f"Peak queries in window: {result['peak_queries']}")
        
        if len(result["indicators"]) >= 2:
            review_count += 1
            print("[REVIEW REQUIRED]")
            for indicator in result["indicators"]:
                print(f"  - {indicator}")
        else:
            print("No multi-indicator review condition met.")
    
    print("\n===== FINAL SUMMARY =====")
    print(f"Clients analysed: {len(grouped)}")
    print(f"Clients flagged for review: {review_count}")
    print("\nThis is heuristic analysis.")
    print("A review result does not establish malicious activity.")
    print(
        "Interpret results using network baselines and "
        "additional endpoint and resolver evidence."
    )
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
