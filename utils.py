"""Input helpers for Smart Event Analyzer."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_events(path: str | Path = "data/events.json") -> list[dict[str, Any]]:
    """Load event records from UTF-8 JSON and validate the top-level shape."""
    with Path(path).open("r", encoding="utf-8") as stream:
        data = json.load(stream)
    if not isinstance(data, list):
        raise ValueError("The events file must contain a JSON array.")
    if any(not isinstance(item, dict) for item in data):
        raise ValueError("Every event must be a JSON object.")
    return data
