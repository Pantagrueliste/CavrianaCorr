#!/usr/bin/env python3
"""
scripts/generate_custom_heatmap.py
Build CustomHeatmap.jsx from the JSX template + CSV data.
The finished file is written to generated/CustomHeatmap.jsx
"""

from __future__ import annotations

import sys

from heatmap_utils import ROOT, generate_heatmap, setup_logging

# ── paths specific to this heatmap variant ─────────────────────
TEMPLATE = ROOT / "templates" / "CustomHeatmap.template.jsx"
OUT_FILE = ROOT / "generated" / "CustomHeatmap.jsx"


def main() -> int:
    """Generate the custom heatmap component."""
    setup_logging()
    return generate_heatmap(TEMPLATE, OUT_FILE)


if __name__ == "__main__":
    sys.exit(main())
