import sys
import unittest
from pathlib import Path

# Set up project root path so python can locate our script modules
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "python"))

from security_log_analyzer import (
    analyze_events,
    validate_events,
)

class TestSecurityLogAnalyzer(unittest.TestCase):

    def test_counts_failed_logins(self):
        """Test that analyze_events correctly tallies total events and failed logins."""
        events = [
            {
                "timestamp": "2026-10-24T09:00:00Z",
                "username": "test_user",
                "event": "login_failed",
                "source_ip": "192.0.2.15",
            },
            {
                "timestamp": "2026-10-24T09:01:00Z",
                "username": "demo_user",
                "event": "login_success",
                "source_ip": "198.51.100.25",
            },
        ]

        summary = analyze_events(events)

        self.assertEqual(summary["total_events"], 2)
        self.assertEqual(summary["failed_login_count"], 1)

    def test_rejects_missing_fields(self):
        """Test that validate_events correctly isolates records missing required keys."""
        events = [
            {
                "timestamp": "2026-10-24T09:00:00Z",
                "username": "test_user",
                "event": "login_failed",
            }
        ]

        valid, invalid = validate_events(events)

        self.assertEqual(len(valid), 0)
        self.assertEqual(len(invalid), 1)

    def test_rejects_non_dictionary_record(self):
        """Test that validate_events rejects raw strings or malformed data types."""
        valid, invalid = validate_events(["not a record"])

        self.assertEqual(len(valid), 0)
        self.assertEqual(len(invalid), 1)

if __name__ == "__main__":
    unittest.main()