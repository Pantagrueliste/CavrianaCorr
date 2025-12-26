#!/usr/bin/env python3
"""
scripts/heatmap_utils.py
Shared utilities for heatmap generation scripts.

This module contains common functions used by both generate_heatmap.py
and generate_custom_heatmap.py to eliminate code duplication.
"""

from __future__ import annotations

import csv
import json
import logging
import re
import sys
from pathlib import Path
from typing import Dict, List

# Configure module logger
logger = logging.getLogger(__name__)

# ── repo structure ──────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
CSV_FILE = ROOT / "data" / "letter_metadata.csv"
OUT_DIR = ROOT / "generated"


def setup_logging(level: int = logging.INFO) -> None:
    """Configure logging for the heatmap scripts."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def load_metadata(csv_path: Path = CSV_FILE) -> List[Dict[str, str | int]]:
    """
    Load letter metadata from CSV file.

    Args:
        csv_path: Path to the CSV file containing letter metadata.

    Returns:
        List of dicts with 'date' (YYYY-MM-DD) and 'value' (word count) keys.

    Raises:
        FileNotFoundError: If the CSV file doesn't exist.
        ValueError: If the CSV is empty or has no valid rows.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    rows: List[Dict[str, str | int]] = []

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
                    logger.warning("Skipping row without date column: %s", r)
                    continue

                if "word_count" not in r:
                    logger.warning("Skipping row without word_count column: %s", r)
                    continue

                # Parse and validate date
                date_parts = r[date_col].split("-")
                if len(date_parts) != 3:
                    logger.warning(
                        "Invalid date format (expected YYYY-MM-DD): %s", r[date_col]
                    )
                    continue

                y, m, d = map(int, date_parts)

                # Parse word count
                word_cnt = int(r["word_count"])

                rows.append({"date": f"{y}-{m:02d}-{d:02d}", "value": word_cnt})
            except ValueError as e:
                logger.warning("Error processing row %s: %s", r, e)
                continue

    if not rows:
        raise ValueError("No valid data rows found in CSV file")

    logger.info("Loaded %d rows from %s", len(rows), csv_path.name)
    return rows


def deduplicate_rows(rows: List[Dict[str, str | int]]) -> List[Dict[str, str | int]]:
    """
    Deduplicate rows by date, keeping the maximum word count for each date.

    Args:
        rows: List of row dicts with 'date' and 'value' keys.

    Returns:
        Deduplicated and sorted list of rows.
    """
    date_map: Dict[str, int] = {}
    for row in rows:
        date = str(row["date"])
        value = int(row["value"])
        if date in date_map:
            date_map[date] = max(date_map[date], value)
        else:
            date_map[date] = value

    deduped = [{"date": date, "value": value} for date, value in date_map.items()]
    deduped.sort(key=lambda x: str(x["date"]))

    if len(deduped) < len(rows):
        logger.info(
            "Deduplicated %d rows to %d unique dates", len(rows), len(deduped)
        )

    return deduped


def inject_years(template: str, years: List[int]) -> str:
    """
    Replace the hard-coded YEARS constant in the template with computed years.

    Args:
        template: The JSX template content.
        years: List of years to inject.

    Returns:
        Modified template with updated YEARS constant.
    """
    pattern = re.compile(r"const YEARS = \[[^\]]+\];")
    return pattern.sub(f"const YEARS = {json.dumps(years)};", template)


def generate_heatmap(
    template_path: Path,
    output_path: Path,
    csv_path: Path = CSV_FILE,
) -> int:
    """
    Generate a heatmap JSX file from a template and CSV data.

    Args:
        template_path: Path to the JSX template file.
        output_path: Path where the generated file will be written.
        csv_path: Path to the CSV file with letter metadata.

    Returns:
        0 on success, 1 on error.
    """
    try:
        # Check if template exists
        if not template_path.exists():
            logger.error("Template file not found: %s", template_path)
            return 1

        # Load and process data
        try:
            rows = load_metadata(csv_path)
            years = sorted({int(str(r["date"])[:4]) for r in rows})
        except (FileNotFoundError, ValueError) as e:
            logger.error("Error loading metadata: %s", e)
            return 1

        # Deduplicate entries for same date
        deduped_rows = deduplicate_rows(rows)

        # Read and patch template
        try:
            jsx = template_path.read_text()
            jsx = inject_years(jsx, years)
            jsx = jsx.replace(
                "/* __DATA_PLACEHOLDER__ */", json.dumps(deduped_rows, indent=2)
            )
        except OSError as e:
            logger.error("Error reading template: %s", e)
            return 1

        # Ensure output folder exists, write file
        try:
            output_path.parent.mkdir(exist_ok=True)
            output_path.write_text(jsx, encoding="utf-8")
            logger.info("✅ Wrote %s", output_path.relative_to(ROOT))
            return 0
        except OSError as e:
            logger.error("Error writing output file: %s", e)
            return 1

    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        return 1
