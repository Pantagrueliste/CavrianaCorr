"""
tests/test_validate_consistency.py
Unit tests for validate_consistency module.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate_consistency import (
    check_duplicate_elements,
    check_namespace,
    check_nested_encoding_desc,
    check_required_elements,
    check_xml_declaration,
    validate_file,
)


class TestCheckXmlDeclaration:
    """Tests for check_xml_declaration function."""

    def test_valid_declaration(self, temp_dir: Path):
        """Test that valid XML declaration passes."""
        content = '<?xml version="1.0" encoding="UTF-8"?>\n<TEI></TEI>'
        errors = check_xml_declaration(temp_dir / "test.xml", content)
        assert len(errors) == 0

    def test_missing_declaration(self, temp_dir: Path):
        """Test that missing XML declaration is detected."""
        content = "<TEI></TEI>"
        errors = check_xml_declaration(temp_dir / "test.xml", content)
        assert len(errors) == 1
        assert "Missing XML declaration" in errors[0]


class TestCheckDuplicateElements:
    """Tests for check_duplicate_elements function."""

    def test_no_duplicates(self, temp_dir: Path):
        """Test that single elements pass."""
        content = "<TEI><teiHeader><encodingDesc/></teiHeader></TEI>"
        errors = check_duplicate_elements(temp_dir / "test.xml", content)
        assert len(errors) == 0

    def test_duplicate_encoding_desc(self, temp_dir: Path):
        """Test that duplicate encodingDesc is detected."""
        content = "<TEI><encodingDesc></encodingDesc><encodingDesc></encodingDesc></TEI>"
        errors = check_duplicate_elements(temp_dir / "test.xml", content)
        assert len(errors) == 1
        assert "encodingDesc" in errors[0]

    def test_duplicate_tei_header(self, temp_dir: Path):
        """Test that duplicate teiHeader is detected."""
        content = "<TEI><teiHeader></teiHeader><teiHeader></teiHeader></TEI>"
        errors = check_duplicate_elements(temp_dir / "test.xml", content)
        assert len(errors) == 1
        assert "teiHeader" in errors[0]


class TestCheckNestedEncodingDesc:
    """Tests for check_nested_encoding_desc function."""

    def test_no_nesting(self, temp_dir: Path):
        """Test that non-nested encodingDesc passes."""
        content = "<TEI><encodingDesc><p>Content</p></encodingDesc></TEI>"
        errors = check_nested_encoding_desc(temp_dir / "test.xml", content)
        assert len(errors) == 0

    def test_nested_encoding_desc(self, temp_dir: Path):
        """Test that nested encodingDesc is detected."""
        content = "<encodingDesc><encodingDesc></encodingDesc></encodingDesc>"
        errors = check_nested_encoding_desc(temp_dir / "test.xml", content)
        assert len(errors) == 1
        assert "Nested" in errors[0]


class TestCheckRequiredElements:
    """Tests for check_required_elements function."""

    def test_all_required_present(self, temp_dir: Path):
        """Test that all required elements pass."""
        content = "<TEI><teiHeader/><text/></TEI>"
        errors = check_required_elements(temp_dir / "test.xml", content)
        assert len(errors) == 0

    def test_missing_tei(self, temp_dir: Path):
        """Test that missing TEI is detected."""
        content = "<doc><teiHeader/><text/></doc>"
        errors = check_required_elements(temp_dir / "test.xml", content)
        assert len(errors) == 1
        assert "TEI" in errors[0]

    def test_missing_text(self, temp_dir: Path):
        """Test that missing text element is detected."""
        content = "<TEI><teiHeader/></TEI>"
        errors = check_required_elements(temp_dir / "test.xml", content)
        assert len(errors) == 1
        assert "text" in errors[0]


class TestCheckNamespace:
    """Tests for check_namespace function."""

    def test_valid_namespace(self, temp_dir: Path):
        """Test that valid namespace passes."""
        content = '<TEI xmlns="http://www.tei-c.org/ns/1.0"></TEI>'
        errors = check_namespace(temp_dir / "test.xml", content)
        assert len(errors) == 0

    def test_missing_namespace(self, temp_dir: Path):
        """Test that missing namespace is detected."""
        content = "<TEI></TEI>"
        errors = check_namespace(temp_dir / "test.xml", content)
        assert len(errors) == 1
        assert "namespace" in errors[0]


class TestValidateFile:
    """Integration tests for validate_file function."""

    def test_valid_file(self, temp_dir: Path):
        """Test that a valid TEI file passes all checks."""
        content = '''<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader></teiHeader>
  <text></text>
</TEI>'''
        file_path = temp_dir / "valid.xml"
        file_path.write_text(content)
        errors = validate_file(file_path)
        assert len(errors) == 0

    def test_multiple_errors(self, temp_dir: Path):
        """Test that multiple errors are detected."""
        content = "<doc></doc>"  # Missing declaration, TEI, teiHeader, text
        file_path = temp_dir / "invalid.xml"
        file_path.write_text(content)
        errors = validate_file(file_path)
        assert len(errors) >= 3  # At least declaration, TEI, teiHeader, text

    def test_nonexistent_file(self, temp_dir: Path):
        """Test that nonexistent file returns error."""
        errors = validate_file(temp_dir / "nonexistent.xml")
        assert len(errors) == 1
        assert "Error reading file" in errors[0]
