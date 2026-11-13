"""Command-line entry point for Smart Event Analyzer."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from analyzer import analyze_events
from utils import load_events
from validator import validate_events


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and analyze infrastructure events.")
    parser.add_argument("--input", default="data/events.json", help="Path to an events JSON file")
    parser.add_argument("--output", help="Optional path for a JSON analysis report")
    args = parser.parse_args()

    valid, invalid = validate_events(load_events(args.input))
    report = {
        "validation": {"valid_count": len(valid), "invalid_count": len(invalid), "invalid_records": invalid},
        "analysis": analyze_events(valid),
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\\n", encoding="utf-8")
    return 0 if not invalid else 1


if __name__ == "__main__":
    raise SystemExit(main())
