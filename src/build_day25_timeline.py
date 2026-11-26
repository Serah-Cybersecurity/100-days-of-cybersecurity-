import csv
import json
from datetime import datetime, timezone
from pathlib import Path

INPUT_FILE = Path("data/training/day25_endpoint_events.jsonl")
OUTPUT_FILE = Path("reports/day25/day25_timeline.csv")
INVALID_FILE = Path("reports/day25/day25_invalid_records.jsonl")

REQUIRED_FIELDS = {
    "timestamp",
    "host",
    "source",
    "event_id",
    "observation",
}

OUTPUT_FIELDS = [
    "timestamp",
    "host",
    "source",
    "event_id",
    "account",
    "logon_id",
    "logon_type",
    "source_ip",
    "process_name",
    "process_guid",
    "parent_process_guid",
    "observation",
]


def parse_timestamp(value):
    """Parse an ISO 8601 timestamp and require timezone information."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Timestamp must be a non-empty ISO 8601 string.")

    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"

    try:
        dt = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"Invalid ISO 8601 timestamp: {value!r}") from exc

    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        raise ValueError(f"Timestamp must include timezone information: {value!r}")

    return dt.astimezone(timezone.utc)


def validate_record(record):
    """Validate required fields, types, and UTC-convertible timestamp."""
    if not isinstance(record, dict):
        raise ValueError("Record must be a JSON object.")

    missing = REQUIRED_FIELDS - set(record.keys())
    if missing:
        raise ValueError(f"Missing required fields: {sorted(missing)}")

    for field in ("host", "source", "observation"):
        val = record.get(field)
        if not isinstance(val, str) or not val.strip():
            raise ValueError(f"Field {field!r} must be a non-empty string.")

    event_id = record.get("event_id")
    if isinstance(event_id, bool) or not isinstance(event_id, int):
        raise ValueError(f"Field 'event_id' must be an integer, got {event_id!r}.")

    parsed_dt = parse_timestamp(record.get("timestamp"))
    return parsed_dt


def load_records(path):
    """Load JSONL records, returning (valid_records_with_dt, invalid_entries)."""
    valid_records = []
    invalid_entries = []

    input_path = Path(path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue

            try:
                parsed = json.loads(stripped)
                parsed_dt = validate_record(parsed)
            except (json.JSONDecodeError, ValueError) as exc:
                invalid_entries.append({
                    "line_number": line_number,
                    "error": str(exc),
                    "raw_line": raw_line.rstrip("\r\n"),
                })
            else:
                normalized = dict(parsed)
                normalized["_parsed_ts"] = parsed_dt
                valid_records.append(normalized)

    return valid_records, invalid_entries


def write_quarantine(invalid_entries, quarantine_path):
    """Write quarantined/malformed entries as JSONL."""
    q_path = Path(quarantine_path)
    q_path.parent.mkdir(parents=True, exist_ok=True)
    with q_path.open("w", encoding="utf-8", newline="\n") as handle:
        for entry in invalid_entries:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def write_timeline(records, output_path):
    """Sort valid records chronologically in UTC and write CSV."""
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    sorted_records = sorted(
        records,
        key=lambda item: (
            item["_parsed_ts"],
            str(item.get("host", "")),
            str(item.get("source", "")),
            int(item.get("event_id", 0)),
        ),
    )

    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for rec in sorted_records:
            row = {field: rec.get(field) for field in OUTPUT_FIELDS}
            row["timestamp"] = rec["_parsed_ts"].strftime("%Y-%m-%dT%H:%M:%SZ")
            writer.writerow(row)

    return sorted_records


def build_timeline(
    input_path=INPUT_FILE,
    output_path=OUTPUT_FILE,
    quarantine_path=INVALID_FILE,
):
    """Execute full load, quarantine, sort, and export workflow."""
    valid_records, invalid_entries = load_records(input_path)
    write_quarantine(invalid_entries, quarantine_path)
    sorted_records = write_timeline(valid_records, output_path)
    return sorted_records, invalid_entries


if __name__ == "__main__":
    valid, invalid = build_timeline()
    print(f"Valid records: {len(valid)} | Invalid/quarantined records: {len(invalid)}")
