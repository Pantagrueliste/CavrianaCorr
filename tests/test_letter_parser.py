"""
tests/test_letter_parser.py
Unit tests for letter_parser module.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from letter_parser import count_words, get_text, process_xml


class TestCountWords:
    """Tests for count_words function."""

    def test_simple_string(self):
        """Test counting words in a simple string."""
        assert count_words("hello world") == 2

    def test_extra_whitespace(self):
        """Test that extra whitespace is normalized."""
        assert count_words("hello    world") == 2

    def test_newlines_and_tabs(self):
        """Test that newlines and tabs are handled."""
        assert count_words("hello\n\tworld\ntest") == 3

    def test_empty_string(self):
        """Test that empty string returns 0."""
        assert count_words("") == 0

    def test_whitespace_only(self):
        """Test that whitespace-only string returns 0."""
        assert count_words("   \n\t  ") == 0


class TestGetText:
    """Tests for get_text function."""

    def test_none_element(self):
        """Test that None element returns empty string."""
        assert get_text(None) == ""

    def test_simple_element(self, temp_dir: Path):
        """Test extracting text from a simple element."""
        from lxml import etree

        elem = etree.fromstring("<p>Hello world</p>")
        assert get_text(elem) == "Hello world"

    def test_nested_elements(self, temp_dir: Path):
        """Test extracting text from nested elements."""
        from lxml import etree

        elem = etree.fromstring("<p>Hello <b>bold</b> text</p>")
        result = get_text(elem)
        assert "Hello" in result
        assert "bold" in result
        assert "text" in result


class TestProcessXml:
    """Tests for process_xml function."""

    def test_valid_letter(self, temp_dir: Path):
        """Test processing a valid TEI letter file."""
        content = '''<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <profileDesc>
      <correspDesc>
        <correspAction type="sent">
          <persName>Filippo Cavriana</persName>
          <placeName>Paris</placeName>
          <date when="1570-07-15"/>
        </correspAction>
        <correspAction type="received">
          <persName>Francesco I</persName>
        </correspAction>
      </correspDesc>
    </profileDesc>
    <fileDesc>
      <sourceDesc>
        <msDesc>
          <msIdentifier>
            <repository>ASF</repository>
            <idno>MP 4597</idno>
          </msIdentifier>
          <msContents>
            <msItem>
              <locus from="123r" to="124v"/>
              <note type="summary">Test summary</note>
            </msItem>
          </msContents>
        </msDesc>
      </sourceDesc>
    </fileDesc>
  </teiHeader>
  <text>
    <body>
      <p>This is the letter body with some words.</p>
    </body>
  </text>
</TEI>'''
        file_path = temp_dir / "1570-07-15.xml"
        file_path.write_text(content)

        result = process_xml(file_path)

        assert result is not None
        assert result["date"] == "1570-07-15"
        assert result["place"] == "Paris"
        assert result["sender"] == "Filippo Cavriana"
        assert result["receiver"] == "Francesco I"
        assert result["repository"] == "ASF"
        assert result["idno"] == "MP 4597"
        assert result["locus"] == "123r-124v"
        assert result["summary"] == "Test summary"
        assert result["word_count"] > 0

    def test_malformed_xml(self, temp_dir: Path):
        """Test that malformed XML returns None."""
        content = "<TEI><unclosed>"
        file_path = temp_dir / "malformed.xml"
        file_path.write_text(content)

        result = process_xml(file_path)
        assert result is None

    def test_missing_elements(self, temp_dir: Path):
        """Test processing file with missing optional elements."""
        content = '''<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader></teiHeader>
  <text><body></body></text>
</TEI>'''
        file_path = temp_dir / "minimal.xml"
        file_path.write_text(content)

        result = process_xml(file_path)

        assert result is not None
        assert result["date"] == ""
        assert result["place"] == ""
        assert result["sender"] == ""
        assert result["word_count"] == 0

    def test_nonexistent_file(self, temp_dir: Path):
        """Test that nonexistent file returns None."""
        result = process_xml(temp_dir / "nonexistent.xml")
        assert result is None
