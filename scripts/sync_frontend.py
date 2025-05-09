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
import argparse
from pathlib import Path

# ── repo structure ──────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
PARENT_DIR = ROOT.parent

# Source files in the backend
GENERATED_HEATMAP = ROOT / "generated" / "CavrianaHeatmap.jsx"
GENERATED_CUSTOM_HEATMAP = ROOT / "generated" / "CustomHeatmap.jsx"
HEATMAP_CSS = ROOT / "assets" / "cavriana-heatmap.css"
CUSTOM_HEATMAP_CSS = ROOT / "assets" / "cavriana-heatmap-custom.css"

# Target locations in the frontend
FRONTEND_DIR = PARENT_DIR / "CavrianaCorr_FrontEnd"
FRONTEND_COMPONENT = FRONTEND_DIR / "src" / "components" / "CavrianaHeatmap.jsx"
FRONTEND_CUSTOM_COMPONENT = FRONTEND_DIR / "src" / "components" / "CustomHeatmap.jsx"
FRONTEND_CSS = FRONTEND_DIR / "src" / "css" / "cavriana-heatmap.css"
FRONTEND_CUSTOM_CSS = FRONTEND_DIR / "src" / "css" / "cavriana-heatmap-custom.css"

def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Sync heatmap to frontend")
    parser.add_argument("--custom", action="store_true", help="Use custom heatmap instead of CalHeatmap")
    return parser.parse_args(args)

def main(args=None):
    """Copy the generated files to the frontend directory."""
    parsed_args = parse_args(args)
    
    # Choose which files to sync based on the --custom flag
    if parsed_args.custom:
        source_component = GENERATED_CUSTOM_HEATMAP
        source_css = CUSTOM_HEATMAP_CSS
        target_component = FRONTEND_CUSTOM_COMPONENT
        target_css = FRONTEND_CUSTOM_CSS
        print("Syncing custom heatmap component...")
    else:
        source_component = GENERATED_HEATMAP
        source_css = HEATMAP_CSS
        target_component = FRONTEND_COMPONENT
        target_css = FRONTEND_CSS
        print("Syncing CalHeatmap component...")
    
    if not source_component.exists():
        print(f"Error: Generated heatmap file not found at {source_component}")
        print("Please run the appropriate generation script first.")
        return 1

    if not FRONTEND_DIR.exists():
        print(f"Error: Frontend directory not found at {FRONTEND_DIR}")
        print("Please ensure the frontend repository is at the correct location.")
        return 1

    # Create component directory if it doesn't exist
    target_component.parent.mkdir(exist_ok=True)
    
    # Create CSS directory if it doesn't exist
    target_css.parent.mkdir(exist_ok=True)

    # Copy the files
    try:
        shutil.copy2(source_component, target_component)
        print(f"✅ Copied heatmap component to {target_component}")
        
        if source_css.exists():
            shutil.copy2(source_css, target_css)
            print(f"✅ Copied CSS file to {target_css}")
        else:
            print(f"Warning: CSS file not found at {source_css}")
            
        return 0
    except Exception as e:
        print(f"Error copying files: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())