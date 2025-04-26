#!/usr/bin/env python3
"""
Generate CavrianaHeatmap.jsx from a fixed template, injecting only the data rows.
Keeps presentation logic in the template so API regressions can’t slip in.
"""

import csv
import json
from datetime import datetime
from pathlib import Path

# ----------------------------------------------------------------------
TEMPLATE_PATH = Path("templates/CavrianaHeatmap.template.jsx")
CSV_PATH      = Path("data/letter_metadata.csv")   # ← new tidy location
OUTPUT_PATH   = Path("CavrianaHeatmap.jsx")        # written at repo root
# ----------------------------------------------------------------------


def load_metadata(csv_path: Path = CSV_PATH) -> list[dict]:
    """Return [{date: <ms>, value: <words>}, …] from the CSV."""
    rows = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            y, m, d = map(int, r["date"].split("-"))
            ms = int(datetime(y, m, d).timestamp()) * 1000  # seconds → ms
            rows.append({"date": ms, "value": int(r["word_count"])})
    return rows


def main() -> None:
    template = TEMPLATE_PATH.read_text()
    rows_json = json.dumps(load_metadata(), indent=2)

    OUTPUT_PATH.write_text(
        template.replace("/* __DATA_PLACEHOLDER__ */", rows_json)
    )
    print("✅  Heat-map component saved to", OUTPUT_PATH)


if __name__ == "__main__":
    main()