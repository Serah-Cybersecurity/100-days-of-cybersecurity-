#!/usr/bin/env python3

"""
Day 15: Offline PCAP Metadata Summary Tool.

Purpose:
    Use TShark to extract selected packet metadata
    from an existing packet capture file.

Scope:
    Offline analysis only.

Privacy:
    Does not extract application payloads or credentials.

Limitations:
    Packet metadata is not a complete picture of
    network behaviour or system security.
"""

import argparse
import csv
import io
import shutil
import subprocess
import sys

from collections import Counter
from pathlib import Path


FIELDS = [
    "frame.number",
    "frame.time_epoch",
    "frame.len",
    "_ws.col.Protocol",
    "eth.src",
    "eth.dst",
    "ip.src",
    "ip.dst",
    "ipv6.src",
    "ipv6.dst",
    "tcp.srcport",
    "tcp.dstport",
    "udp.srcport",
    "udp.dstport",
]


def extract_packet_metadata(capture_path):

    tshark = shutil.which("tshark")

    if tshark is None:

        raise RuntimeError(
            "TShark was not found. "
            "Check whether Wireshark/TShark is installed."
        )

    if not capture_path.is_file():

        raise FileNotFoundError(
            f"Capture file does not exist: {capture_path}"
        )

    command = [
        tshark,
        "-r",
        str(capture_path),
        "-T",
        "fields",
        "-E",
        "header=y",
        "-E",
        "separator=,",
        "-E",
        "quote=d",
    ]

    for field in FIELDS:

        command.extend([
            "-e",
            field,
        ])

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:

        raise RuntimeError(
            result.stderr.strip()
            or "TShark could not process the capture."
        )

    reader = csv.DictReader(
        io.StringIO(result.stdout)
    )

    rows = list(reader)

    return rows


def get_endpoint(row, prefix):

    ip_address = (
        row.get(f"{prefix}.src")
        if prefix == "source"
        else row.get(f"{prefix}.dst")
    )

    return ip_address


def summarise(rows):

    protocol_counts = Counter()
    source_counts = Counter()
    destination_counts = Counter()
    conversations = Counter()

    total_bytes = 0

    for row in rows:

        protocol = (
            row.get("_ws.col.Protocol")
            or "Unknown"
        )

        protocol_counts[protocol] += 1

        source_ip = (
            row.get("ip.src")
            or row.get("ipv6.src")
            or row.get("eth.src")
            or "Unknown"
        )

        destination_ip = (
            row.get("ip.dst")
            or row.get("ipv6.dst")
            or row.get("eth.dst")
            or "Unknown"
        )

        source_counts[source_ip] += 1

        destination_counts[destination_ip] += 1

        source_port = (
            row.get("tcp.srcport")
            or row.get("udp.srcport")
            or ""
        )

        destination_port = (
            row.get("tcp.dstport")
            or row.get("udp.dstport")
            or ""
        )

        source_endpoint = (
            f"{source_ip}:{source_port}"
            if source_port
            else source_ip
        )

        destination_endpoint = (
            f"{destination_ip}:{destination_port}"
            if destination_port
            else destination_ip
        )

        conversation = " <-> ".join(
            sorted([
                source_endpoint,
                destination_endpoint,
            ])
        )

        conversations[conversation] += 1

        try:

            total_bytes += int(
                row.get("frame.len") or 0
            )

        except ValueError:

            pass

    return (
        protocol_counts,
        source_counts,
        destination_counts,
        conversations,
        total_bytes,
    )


def display_results(rows, summary):

    (
        protocol_counts,
        source_counts,
        destination_counts,
        conversations,
        total_bytes,
    ) = summary

    print("\n===== PCAP ANALYSIS SUMMARY =====")

    print(f"Total packets: {len(rows)}")

    print(f"Total observed bytes: {total_bytes}")

    print("\n===== PROTOCOL DISTRIBUTION =====")

    for protocol, count in protocol_counts.most_common(10):

        print(f"{protocol}: {count}")

    print("\n===== TOP SOURCE ENDPOINTS =====")

    for endpoint, count in source_counts.most_common(10):

        print(f"{endpoint}: {count}")

    print("\n===== TOP DESTINATION ENDPOINTS =====")

    for endpoint, count in destination_counts.most_common(10):

        print(f"{endpoint}: {count}")

    print("\n===== TOP COMMUNICATION PAIRS =====")

    for conversation, count in conversations.most_common(10):

        print(f"{conversation}: {count}")

    print("\n===== LIMITATIONS =====")

    print(
        "This report summarises selected packet metadata."
    )

    print(
        "It does not inspect all application payload content."
    )

    print(
        "It does not establish whether communications are malicious."
    )

    print(
        "Interpretation requires capture context and additional evidence."
    )


def main():

    parser = argparse.ArgumentParser(
        description="Summarise metadata from an offline PCAP file."
    )

    parser.add_argument(
        "capture",
        type=Path,
        help="Path to an existing PCAP or PCAPNG file."
    )

    args = parser.parse_args()

    try:

        rows = extract_packet_metadata(args.capture)

        if not rows:

            print(
                "No packet records were extracted.",
                file=sys.stderr,
            )

            return 1

        summary = summarise(rows)

        display_results(rows, summary)

    except (
        RuntimeError,
        FileNotFoundError,
        OSError,
    ) as exc:

        print(
            f"ERROR: {exc}",
            file=sys.stderr,
        )

        return 2

    return 0


if __name__ == "__main__":

    raise SystemExit(main())
