"""Validation rules for infrastructure events."""
from __future__ import annotations

from typing import Any

REQUIRED_FIELDS = ("event_id", "source", "type", "severity", "location")
ALLOWED_SEVERITY = range(1, 11)


def validate_event(event: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        value = event.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append(f"{field} is required")

    severity = event.get("severity")
    if isinstance(severity, bool) or not isinstance(severity, int):
        errors.append("severity must be an integer")
    elif severity not in ALLOWED_SEVERITY:
        errors.append("severity must be between 1 and 10")
    return errors


def validate_events(events: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    valid: list[dict[str, Any]] = []
    invalid: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for event in events:
        errors = validate_event(event)
        event_id = event.get("event_id")
        if isinstance(event_id, str) and event_id in seen_ids:
            errors.append("event_id must be unique")
        elif isinstance(event_id, str):
            seen_ids.add(event_id)
        if errors:
            invalid.append({"event": event, "errors": errors})
        else:
            valid.append(event)
    return valid, invalid
