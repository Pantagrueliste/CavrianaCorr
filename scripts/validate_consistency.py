#!/usr/bin/env python3
"""
scripts/validate_consistency.py
Validate XML consistency across letter files.

Checks for:
- Missing XML declarations
- Duplicate or nested encodingDesc elements
- Missing required TEI elements
- Inconsistent namespace declarations
"""

from __future__ import annotations

import logging
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
LETTERS_DIR = ROOT / "letters"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def check_xml_declaration(file_path: Path, content: str) -> list[str]:
    """Check for proper XML declaration."""
    errors = []
    if not content.strip().startswith("<?xml"):
        errors.append(f"{file_path.name}: Missing XML declaration")
    return errors


def check_duplicate_elements(file_path: Path, content: str) -> list[str]:
    """Check for duplicate structural elements that should appear once."""
    errors = []
    elements_to_check = ["encodingDesc", "teiHeader", "fileDesc", "sourceDesc"]

    for element in elements_to_check:
        # Count opening tags (excluding self-closing)
        pattern = rf"<{element}[>\s]"
        matches = re.findall(pattern, content)
        if len(matches) > 1:
            errors.append(
                f"{file_path.name}: Duplicate <{element}> elements ({len(matches)} found)"
            )

    return errors


def check_nested_encoding_desc(file_path: Path, content: str) -> list[str]:
    """Check for improperly nested encodingDesc elements."""
    errors = []
    # Look for encodingDesc containing another encodingDesc
    pattern = r"<encodingDesc[^>]*>.*?<encodingDesc"
    if re.search(pattern, content, re.DOTALL):
        errors.append(f"{file_path.name}: Nested <encodingDesc> elements detected")
    return errors


def check_required_elements(file_path: Path, content: str) -> list[str]:
    """Check for required TEI elements."""
    errors = []
    required = ["TEI", "teiHeader", "text"]

    for element in required:
        if f"<{element}" not in content:
            errors.append(f"{file_path.name}: Missing required <{element}> element")

    return errors


def check_namespace(file_path: Path, content: str) -> list[str]:
    """Check for proper TEI namespace declaration."""
    errors = []
    if '<TEI xmlns="http://www.tei-c.org/ns/1.0"' not in content:
        # Check for TEI element without namespace
        if "<TEI>" in content or "<TEI " in content:
            errors.append(f"{file_path.name}: TEI element missing namespace declaration")
    return errors


def validate_file(file_path: Path) -> list[str]:
    """Run all consistency checks on a single file."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"{file_path.name}: Error reading file: {e}"]

    errors = []
    errors.extend(check_xml_declaration(file_path, content))
    errors.extend(check_duplicate_elements(file_path, content))
    errors.extend(check_nested_encoding_desc(file_path, content))
    errors.extend(check_required_elements(file_path, content))
    errors.extend(check_namespace(file_path, content))

    return errors


def validate_consistency() -> int:
    """
    Validate XML consistency across all letter files.

    Returns:
        0 if all files pass, 1 if any errors found.
    """
    # Get all letter XML files (exclude authority files)
    letter_files = sorted(
        f
        for f in LETTERS_DIR.glob("*.xml")
        if not f.name.endswith("Names.xml")  # Exclude persNames.xml, placeNames.xml
    )

    if not letter_files:
        logger.warning("No letter files found in %s", LETTERS_DIR)
        return 0

    logger.info("Checking %d letter files for consistency...", len(letter_files))

    all_errors: list[str] = []
    for file_path in letter_files:
        errors = validate_file(file_path)
        all_errors.extend(errors)

    if all_errors:
        logger.error("Found %d consistency issues:", len(all_errors))
        for error in all_errors:
            logger.error("  - %s", error)
        return 1

    logger.info("All files pass consistency checks")
    return 0


def main() -> int:
    """Entry point."""
    return validate_consistency()


if __name__ == "__main__":
    sys.exit(main())
