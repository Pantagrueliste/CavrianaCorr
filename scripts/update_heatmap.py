#!/usr/bin/env python3
"""
scripts/update_heatmap.py
Master script to generate the heatmap and synchronize it with the frontend.
This script runs both generate_heatmap.py and sync_frontend.py in sequence.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# ── repo structure ──────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
GENERATE_SCRIPT = SCRIPT_DIR / "generate_heatmap.py"
SYNC_SCRIPT = SCRIPT_DIR / "sync_frontend.py"

def ensure_executable(script_path):
    """Ensure the script has executable permissions."""
    if not os.access(script_path, os.X_OK):
        os.chmod(script_path, 0o755)  # rwxr-xr-x

def main():
    """Run both scripts in sequence."""
    # Make sure scripts are executable
    ensure_executable(GENERATE_SCRIPT)
    ensure_executable(SYNC_SCRIPT)
    
    print("=== Updating Cavriana Heatmap ===")
    
    # Step 1: Generate the heatmap component
    print("\n-- Step 1: Generating heatmap component --")
    generate_result = subprocess.run([sys.executable, str(GENERATE_SCRIPT)], 
                                   capture_output=True, text=True)
    
    if generate_result.returncode != 0:
        print("Error generating heatmap:")
        print(generate_result.stderr)
        return 1
    
    print(generate_result.stdout)
    
    # Step 2: Sync with frontend
    print("\n-- Step 2: Synchronizing with frontend --")
    sync_result = subprocess.run([sys.executable, str(SYNC_SCRIPT)], 
                               capture_output=True, text=True)
    
    if sync_result.returncode != 0:
        print("Error synchronizing with frontend:")
        print(sync_result.stderr)
        return 1
    
    print(sync_result.stdout)
    
    print("\n✅ Heatmap successfully updated and synchronized with frontend!")
    return 0

if __name__ == "__main__":
    sys.exit(main())