import json
import tempfile
import unittest
from datetime import timezone
from pathlib import Path

from src.build_day25_timeline import (
    build_timeline,
    parse_timestamp,
    validate_record,
)


class TestDay25Timeline(unittest.TestCase):
    def test_utc_timestamp(self):
        result = parse_timestamp("2026-11-26T09:00:00Z")
        self.assertEqual(result.tzinfo, timezone.utc)

    def test_timezone_conversion(self):
        result = parse_timestamp("2026-11-26T12:00:00+03:00")
        self.assertEqual(
            result.isoformat(),
            "2026-11-26T09:00:00+00:00",
        )

    def test_reject_timestamp_without_timezone(self):
        with self.assertRaises(ValueError):
            parse_timestamp("2026-11-26T09:00:00")

    def test_reject_missing_timestamp(self):
        record = {
            "host": "NS-WKS-014",
            "source": "Security",
            "event_id": 4624,
            "observation": "Missing timestamp record",
        }
        with self.assertRaises(ValueError):
            validate_record(record)

    def test_reject_non_integer_event_id(self):
        record = {
            "timestamp": "2026-11-26T09:00:00Z",
            "host": "NS-WKS-014",
            "source": "Security",
            "event_id": "4624",
            "observation": "Training record",
        }
        with self.assertRaises(ValueError):
            validate_record(record)

    def test_reject_boolean_event_id(self):
        record = {
            "timestamp": "2026-11-26T09:00:00Z",
            "host": "NS-WKS-014",
            "source": "Security",
            "event_id": True,
            "observation": "Boolean event_id must fail",
        }
        with self.assertRaises(ValueError):
            validate_record(record)

    def test_reject_missing_host(self):
        record = {
            "timestamp": "2026-11-26T09:00:00Z",
            "source": "Security",
            "event_id": 4624,
            "observation": "Training record",
        }
        with self.assertRaises(ValueError):
            validate_record(record)

    def test_reject_empty_hostname(self):
        record = {
            "timestamp": "2026-11-26T09:00:00Z",
            "host": "   ",
            "source": "Security",
            "event_id": 4624,
            "observation": "Whitespace-only host",
        }
        with self.assertRaises(ValueError):
            validate_record(record)

    def test_accepts_record_with_optional_fields_absent(self):
        minimal_record = {
            "timestamp": "2026-11-26T09:00:00Z",
            "host": "NS-WKS-014",
            "source": "Security",
            "event_id": 4624,
            "observation": "Minimal valid record without optional fields",
        }
        parsed = validate_record(minimal_record)
        self.assertEqual(parsed.tzinfo, timezone.utc)

    def test_quarantines_malformed_jsonl_line(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            jsonl_path = tmp / "sample.jsonl"
            out_csv = tmp / "timeline.csv"
            q_jsonl = tmp / "invalid.jsonl"

            valid_line = json.dumps({
                "timestamp": "2026-11-26T09:00:00Z",
                "host": "NS-WKS-014",
                "source": "Security",
                "event_id": 4624,
                "observation": "Valid event",
            })
            jsonl_path.write_text(f"{valid_line}\n{{bad json\n", encoding="utf-8")

            valid, invalid = build_timeline(jsonl_path, out_csv, q_jsonl)
            self.assertEqual(len(valid), 1)
            self.assertEqual(len(invalid), 1)
            self.assertEqual(invalid[0]["line_number"], 2)


if __name__ == "__main__":
    unittest.main()
