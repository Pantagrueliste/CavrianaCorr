#!/usr/bin/env python3
"""
scripts/generate_heatmap.py
Build CavrianaHeatmap.jsx from the JSX template + CSV data.
The finished file is written to generated/CavrianaHeatmap.jsx
"""

from __future__ import annotations

import sys

from heatmap_utils import ROOT, generate_heatmap, setup_logging

# ── paths specific to this heatmap variant ─────────────────────
TEMPLATE = ROOT / "templates" / "CavrianaHeatmap.template.jsx"
OUT_FILE = ROOT / "generated" / "CavrianaHeatmap.jsx"


def main() -> int:
    """Generate the CalHeatmap-based heatmap component."""
    setup_logging()
    return generate_heatmap(TEMPLATE, OUT_FILE)


if __name__ == "__main__":
    sys.exit(main())
