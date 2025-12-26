#!/usr/bin/env python3
"""
Validate that all entity references in letters exist in authority files.

This script checks that every ref="#..." attribute in letter XML files
has a corresponding xml:id in either persNames.xml or placeNames.xml.

Usage:
    python scripts/validate_references.py

Exit codes:
    0 - All references valid
    1 - Missing references found
"""

import re
import sys
from pathlib import Path

# Paths relative to repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
LETTERS_DIR = REPO_ROOT / "letters"
PERS_NAMES_FILE = LETTERS_DIR / "persNames.xml"
PLACE_NAMES_FILE = LETTERS_DIR / "placeNames.xml"


def extract_xml_ids(file_path: Path) -> set:
    """Extract all xml:id values from an authority file."""
    if not file_path.exists():
        print(f"WARNING: Authority file not found: {file_path}")
        return set()

    content = file_path.read_text(encoding="utf-8")
    # Match xml:id="..." patterns
    ids = set(re.findall(r'xml:id="([^"]+)"', content))
    return ids


def extract_refs(file_path: Path) -> dict:
    """Extract all ref="#..." values from a letter file.

    Returns a dict mapping ref values to line numbers for error reporting.
    """
    refs = {}
    content = file_path.read_text(encoding="utf-8")

    for line_num, line in enumerate(content.split("\n"), start=1):
        # Match ref="#..." patterns (with or without the #)
        for match in re.finditer(r'ref="(?:#)?([^"]+)"', line):
            ref = match.group(1)
            if ref not in refs:
                refs[ref] = []
            refs[ref].append(line_num)

    return refs


def validate_references() -> int:
    """Main validation function.

    Returns:
        0 if all references are valid, 1 if there are missing references.
    """
    print("Validating entity references...")
    print(f"Letters directory: {LETTERS_DIR}")
    print()

    # Load authority IDs
    person_ids = extract_xml_ids(PERS_NAMES_FILE)
    place_ids = extract_xml_ids(PLACE_NAMES_FILE)
    all_authority_ids = person_ids | place_ids

    print(f"Found {len(person_ids)} person IDs in persNames.xml")
    print(f"Found {len(place_ids)} place IDs in placeNames.xml")
    print()

    # Collect all references from letter files
    missing_refs = {}  # ref -> [(file, line_num), ...]
    total_refs = 0

    for xml_file in sorted(LETTERS_DIR.glob("*.xml")):
        # Skip authority files
        if xml_file.name in ["persNames.xml", "placeNames.xml"]:
            continue

        refs = extract_refs(xml_file)
        total_refs += sum(len(lines) for lines in refs.values())

        for ref, line_nums in refs.items():
            if ref not in all_authority_ids:
                if ref not in missing_refs:
                    missing_refs[ref] = []
                for line_num in line_nums:
                    missing_refs[ref].append((xml_file.name, line_num))

    print(f"Checked {total_refs} references across letter files")
    print()

    if not missing_refs:
        print("✓ All references are valid!")
        return 0

    # Report missing references
    print(f"✗ Found {len(missing_refs)} missing references:\n")

    # Categorize by type (pers- vs place- vs other)
    missing_persons = {k: v for k, v in missing_refs.items() if k.startswith("pers-")}
    missing_places = {k: v for k, v in missing_refs.items() if k.startswith("place-")}
    missing_other = {k: v for k, v in missing_refs.items()
                     if not k.startswith("pers-") and not k.startswith("place-")}

    if missing_persons:
        print(f"Missing PERSON references ({len(missing_persons)}):")
        print("  Add these to letters/persNames.xml:")
        for ref in sorted(missing_persons.keys()):
            locations = missing_persons[ref]
            loc_str = ", ".join(f"{f}:{ln}" for f, ln in locations[:3])
            if len(locations) > 3:
                loc_str += f" (+{len(locations) - 3} more)"
            print(f"    - {ref}")
            print(f"      Used in: {loc_str}")
        print()

    if missing_places:
        print(f"Missing PLACE references ({len(missing_places)}):")
        print("  Add these to letters/placeNames.xml:")
        for ref in sorted(missing_places.keys()):
            locations = missing_places[ref]
            loc_str = ", ".join(f"{f}:{ln}" for f, ln in locations[:3])
            if len(locations) > 3:
                loc_str += f" (+{len(locations) - 3} more)"
            print(f"    - {ref}")
            print(f"      Used in: {loc_str}")
        print()

    if missing_other:
        print(f"MALFORMED references ({len(missing_other)}):")
        print("  These don't follow the pers-/place- naming convention:")
        for ref in sorted(missing_other.keys()):
            locations = missing_other[ref]
            loc_str = ", ".join(f"{f}:{ln}" for f, ln in locations[:3])
            if len(locations) > 3:
                loc_str += f" (+{len(locations) - 3} more)"
            print(f"    - {ref}")
            print(f"      Used in: {loc_str}")
        print()

    return 1


if __name__ == "__main__":
    sys.exit(validate_references())
