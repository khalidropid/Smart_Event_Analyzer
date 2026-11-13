"""Aggregations for event severity and operational hotspots."""
from __future__ import annotations

from collections import Counter
from statistics import mean
from typing import Any


def analyze_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    if not events:
        return {"total_events": 0, "average_severity": 0.0, "severity_by_type": {}, "events_by_location": {}, "critical_events": []}

    grouped: dict[str, list[int]] = {}
    for event in events:
        grouped.setdefault(str(event["type"]), []).append(int(event["severity"]))

    severity_by_type = {
        event_type: {"count": len(values), "average_severity": round(mean(values), 2), "max_severity": max(values)}
        for event_type, values in sorted(grouped.items())
    }
    location_counts = Counter(str(event["location"]) for event in events)
    critical = [event for event in events if int(event["severity"]) >= 8]

    return {
        "total_events": len(events),
        "average_severity": round(mean(int(event["severity"]) for event in events), 2),
        "severity_by_type": severity_by_type,
        "events_by_location": dict(sorted(location_counts.items())),
        "critical_events": critical,
    }
