"""
tests/conftest.py
Shared pytest fixtures for CavrianaCorr tests.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_csv(temp_dir: Path) -> Path:
    """Create a sample CSV file with letter metadata."""
    csv_content = """date,place,sender,receiver,repository,idno,locus,word_count,summary
1570-07-15,Paris,Filippo Cavriana,Bartolomeo Concino,ASF,MP 4597,123r-124v,500,Test letter 1
1570-07-29,Paris,Filippo Cavriana,Francesco I,ASF,MP 4597,125r-126v,750,Test letter 2
1570-07-29,Paris,Filippo Cavriana,Francesco I,ASF,MP 4597,127r-128v,600,Duplicate date
1571-01-14,Nevers,Filippo Cavriana,Guglielmo Gonzaga,ASMn,AG 654,200r-201v,400,Test letter 3
"""
    csv_path = temp_dir / "test_metadata.csv"
    csv_path.write_text(csv_content)
    return csv_path


@pytest.fixture
def sample_template(temp_dir: Path) -> Path:
    """Create a sample JSX template file."""
    template_content = """import React from 'react';

const YEARS = [1570, 1571];

const data = /* __DATA_PLACEHOLDER__ */;

export default function Heatmap() {
  return <div>{JSON.stringify(data)}</div>;
}
"""
    template_path = temp_dir / "test_template.jsx"
    template_path.write_text(template_content)
    return template_path


@pytest.fixture
def sample_authority_files(temp_dir: Path) -> tuple[Path, Path]:
    """Create sample authority XML files."""
    letters_dir = temp_dir / "letters"
    letters_dir.mkdir()

    pers_content = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <text>
    <body>
      <listPerson>
        <person xml:id="pers-cavriana-f">
          <persName>Filippo Cavriana</persName>
        </person>
        <person xml:id="pers-medici-f">
          <persName>Francesco I de' Medici</persName>
        </person>
      </listPerson>
    </body>
  </text>
</TEI>
"""
    pers_path = letters_dir / "persNames.xml"
    pers_path.write_text(pers_content)

    place_content = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <text>
    <body>
      <listPlace>
        <place xml:id="place-paris">
          <placeName>Paris</placeName>
        </place>
        <place xml:id="place-firenze">
          <placeName>Firenze</placeName>
        </place>
      </listPlace>
    </body>
  </text>
</TEI>
"""
    place_path = letters_dir / "placeNames.xml"
    place_path.write_text(place_content)

    return pers_path, place_path
