#!/usr/bin/env python3
"""
scripts/clean_legacy_heatmap.py
Clean up legacy heatmap files after migrating to the custom implementation.
This script moves old files to a backup directory rather than deleting them outright.
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# ── repo structure ──────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
PARENT_DIR = ROOT.parent

# Create a backup directory with timestamp
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = ROOT / "backups" / f"legacy_heatmap_{TIMESTAMP}"

# Files to be moved (not deleted)
FILES_TO_BACKUP = [
    # Backend legacy files
    ROOT / "generated" / "CavrianaHeatmap.jsx",
    # Don't remove the template in case it's needed later
    # ROOT / "templates" / "CavrianaHeatmap.template.jsx",
    # Don't remove the generation script in case it's needed later
    # ROOT / "scripts" / "generate_heatmap.py",
    # ROOT / "scripts" / "update_heatmap.py",
]

# Frontend files - list but don't remove automatically
FRONTEND_DIR = PARENT_DIR / "CavrianaCorr_FrontEnd"
FRONTEND_FILES_TO_CHECK = [
    FRONTEND_DIR / "src" / "components" / "CavrianaHeatmap.jsx",
    FRONTEND_DIR / "src" / "components" / "FixedCavrianaHeatmap.jsx",  
    FRONTEND_DIR / "src" / "css" / "cavriana-heatmap.css",
    FRONTEND_DIR / "static" / "js" / "cal-heatmap-init.js",
]

def backup_file(file_path, backup_dir):
    """Back up a file to the specified directory, preserving its relative path."""
    if not file_path.exists():
        print(f"  • Skipping (not found): {file_path}")
        return False
        
    # Create the same directory structure in the backup
    relative_path = file_path.relative_to(ROOT if str(file_path).startswith(str(ROOT)) else PARENT_DIR)
    backup_path = backup_dir / relative_path
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy the file
    shutil.copy2(file_path, backup_path)
    print(f"  • Backed up: {file_path}")
    return True

def main():
    print(f"🔍 Starting cleanup of legacy heatmap files")
    print(f"📦 Backing up files to: {BACKUP_DIR}")
    
    # Create backup directory
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    # Backup backend files
    print("\n🔄 Backing up backend files:")
    backed_up_count = 0
    for file_path in FILES_TO_BACKUP:
        if backup_file(file_path, BACKUP_DIR):
            backed_up_count += 1
    
    # Check frontend files
    print("\n🔍 Checking frontend files (not automatically backed up):")
    frontend_exists_count = 0
    for file_path in FRONTEND_FILES_TO_CHECK:
        if file_path.exists():
            print(f"  • Found: {file_path}")
            frontend_exists_count += 1
        else:
            print(f"  • Not found: {file_path}")
    
    # Summary
    print("\n📋 Summary:")
    print(f"  • Backed up {backed_up_count} backend files")
    print(f"  • Found {frontend_exists_count} frontend files that might need manual review")
    
    print("\n✅ Files backed up successfully. You can now manually remove the files that are no longer needed.")
    print("   Frontend files should be manually checked and removed as needed.")
    print(f"   Backup location: {BACKUP_DIR}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())