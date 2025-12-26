"""
tests/test_validate_references.py
Unit tests for validate_references module.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate_references import extract_refs, extract_xml_ids


class TestExtractXmlIds:
    """Tests for extract_xml_ids function."""

    def test_extracts_person_ids(self, sample_authority_files):
        """Test extracting person IDs from authority file."""
        pers_path, _ = sample_authority_files
        ids = extract_xml_ids(pers_path)
        assert "pers-cavriana-f" in ids
        assert "pers-medici-f" in ids

    def test_extracts_place_ids(self, sample_authority_files):
        """Test extracting place IDs from authority file."""
        _, place_path = sample_authority_files
        ids = extract_xml_ids(place_path)
        assert "place-paris" in ids
        assert "place-firenze" in ids

    def test_missing_file_returns_empty(self, temp_dir: Path):
        """Test that missing file returns empty set."""
        ids = extract_xml_ids(temp_dir / "nonexistent.xml")
        assert ids == set()


class TestExtractRefs:
    """Tests for extract_refs function."""

    def test_extracts_refs_with_hash(self, temp_dir: Path):
        """Test extracting refs that include # prefix."""
        xml_content = """<?xml version="1.0"?>
<TEI>
  <text>
    <persName ref="#pers-cavriana-f">Cavriana</persName>
    <placeName ref="#place-paris">Paris</placeName>
  </text>
</TEI>
"""
        xml_path = temp_dir / "test.xml"
        xml_path.write_text(xml_content)
        refs = extract_refs(xml_path)
        assert "pers-cavriana-f" in refs
        assert "place-paris" in refs

    def test_extracts_refs_without_hash(self, temp_dir: Path):
        """Test extracting refs that don't have # prefix."""
        xml_content = """<?xml version="1.0"?>
<TEI>
  <persName ref="pers-medici-f">Medici</persName>
</TEI>
"""
        xml_path = temp_dir / "test.xml"
        xml_path.write_text(xml_content)
        refs = extract_refs(xml_path)
        assert "pers-medici-f" in refs

    def test_tracks_line_numbers(self, temp_dir: Path):
        """Test that line numbers are tracked for each ref."""
        xml_content = """<?xml version="1.0"?>
<TEI>
  <persName ref="#pers-cavriana-f">Cavriana</persName>
</TEI>
"""
        xml_path = temp_dir / "test.xml"
        xml_path.write_text(xml_content)
        refs = extract_refs(xml_path)
        # The ref should be on line 3
        assert 3 in refs["pers-cavriana-f"]

    def test_multiple_refs_same_id(self, temp_dir: Path):
        """Test handling multiple occurrences of same ref."""
        xml_content = """<?xml version="1.0"?>
<TEI>
  <persName ref="#pers-cavriana-f">First</persName>
  <persName ref="#pers-cavriana-f">Second</persName>
</TEI>
"""
        xml_path = temp_dir / "test.xml"
        xml_path.write_text(xml_content)
        refs = extract_refs(xml_path)
        assert len(refs["pers-cavriana-f"]) == 2


class TestIntegration:
    """Integration tests for reference validation."""

    def test_valid_references(self, temp_dir: Path, sample_authority_files):
        """Test that valid references pass validation."""
        pers_path, place_path = sample_authority_files
        letters_dir = pers_path.parent

        # Create a letter with valid references
        letter_content = """<?xml version="1.0"?>
<TEI>
  <text>
    <persName ref="#pers-cavriana-f">Cavriana</persName>
    <placeName ref="#place-paris">Paris</placeName>
  </text>
</TEI>
"""
        letter_path = letters_dir / "1570-01-01.xml"
        letter_path.write_text(letter_content)

        # Extract and check
        person_ids = extract_xml_ids(pers_path)
        place_ids = extract_xml_ids(place_path)
        all_ids = person_ids | place_ids

        refs = extract_refs(letter_path)
        missing = set(refs.keys()) - all_ids

        assert len(missing) == 0

    def test_invalid_references_detected(self, temp_dir: Path, sample_authority_files):
        """Test that invalid references are detected."""
        pers_path, place_path = sample_authority_files
        letters_dir = pers_path.parent

        # Create a letter with an invalid reference
        letter_content = """<?xml version="1.0"?>
<TEI>
  <text>
    <persName ref="#pers-nonexistent">Unknown</persName>
  </text>
</TEI>
"""
        letter_path = letters_dir / "1570-01-01.xml"
        letter_path.write_text(letter_content)

        # Extract and check
        person_ids = extract_xml_ids(pers_path)
        place_ids = extract_xml_ids(place_path)
        all_ids = person_ids | place_ids

        refs = extract_refs(letter_path)
        missing = set(refs.keys()) - all_ids

        assert "pers-nonexistent" in missing
