#!/usr/bin/env python3
"""
scripts/generate_custom_heatmap.py
Build CustomHeatmap.jsx from the JSX template + CSV data.
The finished file is written to generated/CustomHeatmap.jsx
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional

# ── repo structure ──────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT       = SCRIPT_DIR.parent
TEMPLATE   = ROOT / "templates" / "CustomHeatmap.template.jsx"
CSV_FILE   = ROOT / "data"      / "letter_metadata.csv"
OUT_DIR    = ROOT / "generated"
OUT_FILE   = OUT_DIR / "CustomHeatmap.jsx"

# ── helpers ─────────────────────────────────────────────────────
def load_metadata(csv_path: Path = CSV_FILE) -> List[Dict]:
    """Return rows as [{'date':'YYYY-MM-DD', 'value': <int>}, …]."""
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
    rows: List[Dict] = []

    try:
        with csv_path.open(encoding="utf-8-sig", newline="") as fh:
            rdr = csv.DictReader(fh)
            
            # Check for required columns
            first_row = next(rdr, None)
            if first_row is None:
                raise ValueError("CSV file is empty")
                
            # Put the reader back at the beginning
            fh.seek(0)
            rdr = csv.DictReader(fh)
            
            # Process rows
            for r in rdr:
                try:
                    date_col = next((c for c in r if "date" in c.lower()), None)
                    if not date_col:
                        print(f"Warning: Skipping row without date column: {r}", file=sys.stderr)
                        continue
                        
                    if "word_count" not in r:
                        print(f"Warning: Skipping row without word_count column: {r}", file=sys.stderr)
                        continue
                        
                    # Parse and validate date
                    date_parts = r[date_col].split("-")
                    if len(date_parts) != 3:
                        print(f"Warning: Invalid date format (expected YYYY-MM-DD): {r[date_col]}", file=sys.stderr)
                        continue
                        
                    y, m, d = map(int, date_parts)
                    
                    # Parse word count
                    word_cnt = int(r["word_count"])
                    
                    rows.append({"date": f"{y}-{m:02d}-{d:02d}", "value": word_cnt})
                except ValueError as e:
                    print(f"Warning: Error processing row {r}: {e}", file=sys.stderr)
                    continue
                
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

    if not rows:
        raise ValueError("No valid data rows found in CSV file")
        
    return rows


def inject_years(template: str, years: List[int]) -> str:
    """Replace the hard-coded YEARS constant with the one we computed."""
    pattern = re.compile(r"const YEARS = \[[^\]]+\];")
    return pattern.sub(f"const YEARS = {json.dumps(years)};", template)


# ── main build routine ──────────────────────────────────────────
def main() -> int:
    try:
        # Check if template exists
        if not TEMPLATE.exists():
            print(f"Error: Template file not found: {TEMPLATE}", file=sys.stderr)
            return 1
            
        # Load and process data
        try:
            rows = load_metadata()
            years = sorted({int(r["date"][:4]) for r in rows})
        except Exception as e:
            print(f"Error loading metadata: {e}", file=sys.stderr)
            return 1

        # Handle duplicate entries for same date (like 1570-07-29) by ensuring consistent order
        # Group by date and merge multiple entries by summing their values
        date_map = {}
        for row in rows:
            date = row["date"]
            value = row["value"]
            if date in date_map:
                # For dates with multiple entries, we'll use the maximum value
                # This ensures consistent data representation
                date_map[date] = max(date_map[date], value)
            else:
                date_map[date] = value
                
        # Rebuild rows with deduped data
        deduped_rows = [{"date": date, "value": value} for date, value in date_map.items()]
        # Sort by date for consistency
        deduped_rows.sort(key=lambda x: x["date"])

        # read/patch template
        try:
            jsx = TEMPLATE.read_text()
            jsx = inject_years(jsx, years)
            jsx = jsx.replace("/* __DATA_PLACEHOLDER__ */",
                             json.dumps(deduped_rows, indent=2))
        except Exception as e:
            print(f"Error processing template: {e}", file=sys.stderr)
            return 1

        # ensure output folder exists, write file
        try:
            OUT_DIR.mkdir(exist_ok=True)
            OUT_FILE.write_text(jsx, encoding="utf-8")
            print(f"✅ Wrote {OUT_FILE.relative_to(ROOT)}")
            return 0
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            return 1
            
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())