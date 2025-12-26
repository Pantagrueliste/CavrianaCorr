"""
tests/test_heatmap_utils.py
Unit tests for heatmap_utils module.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from heatmap_utils import (
    deduplicate_rows,
    generate_heatmap,
    inject_years,
    load_metadata,
)


class TestLoadMetadata:
    """Tests for load_metadata function."""

    def test_load_valid_csv(self, sample_csv: Path):
        """Test loading a valid CSV file."""
        rows = load_metadata(sample_csv)
        assert len(rows) == 4
        assert rows[0]["date"] == "1570-07-15"
        assert rows[0]["value"] == 500

    def test_load_missing_csv(self, temp_dir: Path):
        """Test error when CSV doesn't exist."""
        with pytest.raises(FileNotFoundError):
            load_metadata(temp_dir / "nonexistent.csv")

    def test_load_empty_csv(self, temp_dir: Path):
        """Test error when CSV is empty."""
        empty_csv = temp_dir / "empty.csv"
        empty_csv.write_text("")
        with pytest.raises(ValueError, match="empty"):
            load_metadata(empty_csv)

    def test_normalizes_date_format(self, temp_dir: Path):
        """Test that dates are normalized to YYYY-MM-DD."""
        csv_content = """date,word_count
1570-7-5,100
"""
        csv_path = temp_dir / "dates.csv"
        csv_path.write_text(csv_content)
        rows = load_metadata(csv_path)
        assert rows[0]["date"] == "1570-07-05"


class TestDeduplicateRows:
    """Tests for deduplicate_rows function."""

    def test_no_duplicates(self):
        """Test with unique dates."""
        rows = [
            {"date": "1570-07-15", "value": 500},
            {"date": "1570-07-29", "value": 750},
        ]
        result = deduplicate_rows(rows)
        assert len(result) == 2

    def test_keeps_max_value(self):
        """Test that duplicates keep maximum value."""
        rows = [
            {"date": "1570-07-29", "value": 600},
            {"date": "1570-07-29", "value": 750},
            {"date": "1570-07-29", "value": 500},
        ]
        result = deduplicate_rows(rows)
        assert len(result) == 1
        assert result[0]["value"] == 750

    def test_sorts_by_date(self):
        """Test that results are sorted by date."""
        rows = [
            {"date": "1571-01-14", "value": 400},
            {"date": "1570-07-15", "value": 500},
            {"date": "1570-07-29", "value": 750},
        ]
        result = deduplicate_rows(rows)
        assert result[0]["date"] == "1570-07-15"
        assert result[1]["date"] == "1570-07-29"
        assert result[2]["date"] == "1571-01-14"


class TestInjectYears:
    """Tests for inject_years function."""

    def test_replaces_years_constant(self):
        """Test replacing YEARS constant in template."""
        template = "const YEARS = [1568, 1569];"
        result = inject_years(template, [1570, 1571, 1572])
        assert result == "const YEARS = [1570, 1571, 1572];"

    def test_preserves_surrounding_content(self):
        """Test that surrounding content is preserved."""
        template = "// Header\nconst YEARS = [1568];\n// Footer"
        result = inject_years(template, [1570])
        assert "// Header" in result
        assert "// Footer" in result


class TestGenerateHeatmap:
    """Tests for generate_heatmap function."""

    def test_generates_output_file(
        self, temp_dir: Path, sample_csv: Path, sample_template: Path
    ):
        """Test that output file is generated."""
        output_path = temp_dir / "output.jsx"
        result = generate_heatmap(sample_template, output_path, sample_csv)
        assert result == 0
        assert output_path.exists()

    def test_injects_data(
        self, temp_dir: Path, sample_csv: Path, sample_template: Path
    ):
        """Test that data is injected into template."""
        output_path = temp_dir / "output.jsx"
        generate_heatmap(sample_template, output_path, sample_csv)
        content = output_path.read_text()
        # Should contain the data, not the placeholder
        assert "__DATA_PLACEHOLDER__" not in content
        assert "1570-07-15" in content

    def test_updates_years(
        self, temp_dir: Path, sample_csv: Path, sample_template: Path
    ):
        """Test that YEARS constant is updated."""
        output_path = temp_dir / "output.jsx"
        generate_heatmap(sample_template, output_path, sample_csv)
        content = output_path.read_text()
        assert "[1570, 1571]" in content

    def test_missing_template_returns_error(self, temp_dir: Path, sample_csv: Path):
        """Test error return when template is missing."""
        result = generate_heatmap(
            temp_dir / "missing.jsx", temp_dir / "output.jsx", sample_csv
        )
        assert result == 1

    def test_creates_output_directory(
        self, temp_dir: Path, sample_csv: Path, sample_template: Path
    ):
        """Test that output directory is created if needed."""
        output_path = temp_dir / "subdir" / "output.jsx"
        result = generate_heatmap(sample_template, output_path, sample_csv)
        assert result == 0
        assert output_path.exists()
