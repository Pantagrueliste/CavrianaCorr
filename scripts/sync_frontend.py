#!/usr/bin/env python3
"""
scripts/sync_frontend.py
Synchronizes the generated heatmap component with the frontend.
This script should be run after generate_heatmap.py to ensure
the frontend has the latest version of the heatmap.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

# ── repo structure ──────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
PARENT_DIR = ROOT.parent

# Source files in the backend
GENERATED_HEATMAP = ROOT / "generated" / "CavrianaHeatmap.jsx"
HEATMAP_CSS = ROOT / "assets" / "cavriana-heatmap.css"

# Target locations in the frontend
FRONTEND_DIR = PARENT_DIR / "CavrianaCorr_FrontEnd"
FRONTEND_COMPONENT = FRONTEND_DIR / "src" / "components" / "CavrianaHeatmap.jsx"
FRONTEND_CSS = FRONTEND_DIR / "src" / "css" / "cavriana-heatmap.css"

def main():
    """Copy the generated files to the frontend directory."""
    if not GENERATED_HEATMAP.exists():
        print(f"Error: Generated heatmap file not found at {GENERATED_HEATMAP}")
        print("Please run scripts/generate_heatmap.py first.")
        return 1

    if not FRONTEND_DIR.exists():
        print(f"Error: Frontend directory not found at {FRONTEND_DIR}")
        print("Please ensure the frontend repository is at the correct location.")
        return 1

    # Create component directory if it doesn't exist
    FRONTEND_COMPONENT.parent.mkdir(exist_ok=True)
    
    # Create CSS directory if it doesn't exist
    FRONTEND_CSS.parent.mkdir(exist_ok=True)

    # Copy the files
    try:
        shutil.copy2(GENERATED_HEATMAP, FRONTEND_COMPONENT)
        print(f"✅ Copied heatmap component to {FRONTEND_COMPONENT}")
        
        if HEATMAP_CSS.exists():
            shutil.copy2(HEATMAP_CSS, FRONTEND_CSS)
            print(f"✅ Copied CSS file to {FRONTEND_CSS}")
        else:
            print(f"Warning: CSS file not found at {HEATMAP_CSS}")
            
        return 0
    except Exception as e:
        print(f"Error copying files: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())