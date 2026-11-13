import unittest

from analyzer import analyze_events
from validator import validate_events


class SmartEventAnalyzerTests(unittest.TestCase):
    def test_validation_and_duplicate_ids(self):
        rows = [
            {"event_id": "E1", "source": "host1", "type": "cpu", "severity": 8, "location": "dc1"},
            {"event_id": "E1", "source": "host2", "type": "disk", "severity": 4, "location": "dc2"},
            {"event_id": "E3", "source": "host3", "type": "ram", "severity": 11, "location": "dc2"},
        ]
        valid, invalid = validate_events(rows)
        self.assertEqual(len(valid), 1)
        self.assertEqual(len(invalid), 2)

    def test_aggregations(self):
        rows = [
            {"event_id": "E1", "source": "h1", "type": "cpu", "severity": 8, "location": "dc1"},
            {"event_id": "E2", "source": "h2", "type": "cpu", "severity": 6, "location": "dc1"},
        ]
        report = analyze_events(rows)
        self.assertEqual(report["total_events"], 2)
        self.assertEqual(report["average_severity"], 7)
        self.assertEqual(report["events_by_location"], {"dc1": 2})
        self.assertEqual(len(report["critical_events"]), 1)


if __name__ == "__main__":
    unittest.main()
