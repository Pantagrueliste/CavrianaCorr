#!/usr/bin/env python3
"""
scripts/generate_heatmap.py
Build CavrianaHeatmap.jsx from the JSX template + CSV data.
The finished file is written to generated/CavrianaHeatmap.jsx
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import List, Dict

# ── repo structure ──────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT       = SCRIPT_DIR.parent
TEMPLATE   = ROOT / "templates" / "CavrianaHeatmap.template.jsx"
CSV_FILE   = ROOT / "data"      / "letter_metadata.csv"
OUT_DIR    = ROOT / "generated"
OUT_FILE   = OUT_DIR / "CavrianaHeatmap.jsx"

# ── helpers ─────────────────────────────────────────────────────
def load_metadata(csv_path: Path = CSV_FILE) -> List[Dict]:
    """Return rows as [{'date':'YYYY-MM-DD', 'value': <int>}, …]."""
    rows: List[Dict] = []

    with csv_path.open(encoding="utf-8-sig", newline="") as fh:
        rdr = csv.DictReader(fh)
        for r in rdr:
            date_col = next((c for c in r if "date" in c.lower()), None)
            if not date_col:
                continue                                           # skip bad row
            y, m, d  = map(int, r[date_col].split("-"))
            word_cnt = int(r["word_count"])
            rows.append({"date": f"{y}-{m:02d}-{d:02d}", "value": word_cnt})

    return rows


def inject_years(template: str, years: List[int]) -> str:
    """Replace the hard-coded YEARS constant with the one we computed."""
    pattern = re.compile(r"const YEARS = \[[^\]]+\];")
    return pattern.sub(f"const YEARS = {json.dumps(years)};", template)


# ── main build routine ──────────────────────────────────────────
def main() -> None:
    rows   = load_metadata()
    years  = sorted({int(r["date"][:4]) for r in rows})

    # read/patch template
    jsx    = TEMPLATE.read_text()
    jsx    = inject_years(jsx, years)
    jsx    = jsx.replace("/* __DATA_PLACEHOLDER__ */",
                         json.dumps(rows, indent=2))

    # ensure output folder exists, write file
    OUT_DIR.mkdir(exist_ok=True)
    OUT_FILE.write_text(jsx, encoding="utf-8")
    print("✅ wrote", OUT_FILE.relative_to(ROOT))


if __name__ == "__main__":
    main()
