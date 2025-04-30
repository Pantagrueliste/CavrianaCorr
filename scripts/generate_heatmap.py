#!/usr/bin/env python3
"""
Generate CavrianaHeatmap.jsx from a fixed template, injecting only the data rows.
Keeps presentation logic in the template so API regressions can't slip in.
"""

import csv
import json
from datetime import datetime
from pathlib import Path

# ----------------------------------------------------------------------
# Use the correct relative path based on where the script is being run from
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent

TEMPLATE_PATH = REPO_ROOT / "templates" / "CavrianaHeatmap.template.jsx"
CSV_PATH      = REPO_ROOT / "data" / "letter_metadata.csv"
OUTPUT_PATH   = REPO_ROOT / "CavrianaHeatmap.jsx"
# ----------------------------------------------------------------------

def load_metadata(csv_path: Path = CSV_PATH) -> list[dict]:
    """Return data in a format Cal-Heatmap can use."""
    rows = []
    
    print(f"CSV path: {csv_path}")
    print(f"CSV exists: {csv_path.exists()}")
    
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        
        for r in reader:
            # Check for the date column
            date_col = next((col for col in r.keys() if 'date' in col.lower()), None)
            if not date_col:
                print(f"Warning: No date column found in row: {r}")
                continue
            
            # Process the date
            date_str = r[date_col]
            
            # Extract year, month, day
            y, m, d = map(int, date_str.split("-"))
            
            # Create a key in format "YYYY-MM-DD" for Cal-Heatmap
            date_key = f"{y}-{m:02d}-{d:02d}"
            
            # Get the word count
            word_count = int(r['word_count'])
            
            rows.append({"date": date_key, "value": word_count})
    
    print(f"Processed {len(rows)} rows of data")
    if rows:
        print(f"Sample data: {rows[0]}")
    
    return rows


def main() -> None:
    # Print debug information
    print(f"Current directory: {Path.cwd()}")
    print(f"Template path: {TEMPLATE_PATH}")
    print(f"Template exists: {TEMPLATE_PATH.exists()}")
    
    # Read the template
    template = TEMPLATE_PATH.read_text()
    
    # Prepare the data
    data = load_metadata()
    
    # Create appropriate YEARS list based on the data
    if data:
        years = sorted(set(int(item["date"].split("-")[0]) for item in data))
        print(f"Years in data: {years}")
        years_json = json.dumps(years)
        
        # Update the YEARS constant in the template
        template = template.replace("const YEARS = [1568, 1569, 1570, 1571];", f"const YEARS = {years_json};")
    
    # Format the data as JSON
    rows_json = json.dumps(data, indent=2)

    # Create the output file
    OUTPUT_PATH.write_text(
        template.replace("/* __DATA_PLACEHOLDER__ */", rows_json)
    )
    print("✅  Heat-map component saved to", OUTPUT_PATH)


if __name__ == "__main__":
    main()