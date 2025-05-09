#!/usr/bin/env python3
"""
scripts/update_custom_heatmap.py
Run both the generation and sync scripts to update the custom heatmap.
"""

import os
import sys
import importlib.util
from pathlib import Path

# ── repo structure ──────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
GENERATE_SCRIPT = SCRIPT_DIR / "generate_custom_heatmap.py"
SYNC_SCRIPT = SCRIPT_DIR / "sync_frontend.py"

# Import and run the generation script
def run_generate():
    print("Step 1: Generating custom heatmap component...")
    if not GENERATE_SCRIPT.exists():
        print(f"Error: Script not found: {GENERATE_SCRIPT}", file=sys.stderr)
        return 1
    
    spec = importlib.util.spec_from_file_location("generate_module", GENERATE_SCRIPT)
    generate_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generate_module)
    
    return generate_module.main()

# Import and run the sync script
def run_sync():
    print("Step 2: Syncing custom heatmap to frontend...")
    if not SYNC_SCRIPT.exists():
        print(f"Error: Script not found: {SYNC_SCRIPT}", file=sys.stderr)
        return 1
    
    spec = importlib.util.spec_from_file_location("sync_module", SYNC_SCRIPT)
    sync_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sync_module)
    
    # Call the sync function with the custom parameter
    # Note: We're assuming sync_module.main() can be called directly
    return sync_module.main(["--custom"])

def main():
    # Run generation
    generate_result = run_generate()
    if generate_result != 0:
        print("Error generating custom heatmap component", file=sys.stderr)
        return generate_result
    
    # Run sync
    sync_result = run_sync()
    if sync_result != 0:
        print("Error syncing custom heatmap to frontend", file=sys.stderr)
        return sync_result
    
    print("✅ Custom heatmap updated and synced successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())