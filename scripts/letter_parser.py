#!/usr/bin/env python3
"""
scripts/letter_parser.py
Parse TEI-XML letter files and extract metadata to CSV.
"""

from __future__ import annotations

import csv
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from lxml import etree

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# ── locate repo root ────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_CSV = REPO_ROOT / "data" / "letter_metadata.csv"
LETTERS = REPO_ROOT / "letters"
# ────────────────────────────────────────────────────────────────────────

EXCLUDE = {"persNames.xml", "placeNames.xml"}
NS = {"tei": "http://www.tei-c.org/ns/1.0"}


def count_words(text: str) -> int:
    """Count words in a string after normalizing whitespace."""
    return len(re.sub(r"\s+", " ", text).strip().split())


def get_text(elem: Optional[etree._Element]) -> str:
    """Recursively extract text content from an XML element."""
    if elem is None:
        return ""
    txt = elem.text or ""
    for child in elem:
        txt += " " + get_text(child)
    if elem.tail:
        txt += " " + elem.tail
    return txt.strip()


def count_body_words(body_elem: etree._Element) -> int:
    """Count words in the letter body."""
    txt = " ".join(
        get_text(e)
        for e in body_elem.xpath(
            ".//tei:p | .//tei:div | .//tei:opener | .//tei:closer",
            namespaces=NS,
        )
    )
    return count_words(txt)


def process_xml(path: Path) -> Optional[Dict[str, Any]]:
    """
    Parse a TEI-XML letter file and extract metadata.

    Args:
        path: Path to the XML file.

    Returns:
        Dictionary with extracted metadata, or None on error.
    """
    try:
        root = etree.parse(str(path)).getroot()

        def q(xp: str) -> List[etree._Element]:
            return root.xpath(xp, namespaces=NS)

        date = q("//tei:correspAction[@type='sent']/tei:date")
        place = q("//tei:correspAction[@type='sent']/tei:placeName")
        sender = q("//tei:correspAction[@type='sent']/tei:persName")
        receiver = q("//tei:correspAction[@type='received']/tei:persName")
        repo = q("//tei:msIdentifier/tei:repository")
        idno = q("//tei:msIdentifier/tei:idno")
        locus_elem = q("//tei:msItem/tei:locus")
        summary = q("//tei:note[@type='summary']")
        body = q("//tei:text/tei:body")

        locus = ""
        if locus_elem:
            fr, to = locus_elem[0].get("from"), locus_elem[0].get("to")
            locus = f"{fr}-{to}" if fr and to else get_text(locus_elem[0])

        word_count = count_body_words(body[0]) if body else 0

        return {
            "date": date[0].get("when") if date else "",
            "place": get_text(place[0]) if place else "",
            "sender": get_text(sender[0]) if sender else "",
            "receiver": get_text(receiver[0]) if receiver else "",
            "repository": get_text(repo[0]) if repo else "",
            "idno": get_text(idno[0]) if idno else "",
            "locus": locus,
            "word_count": word_count,
            "summary": get_text(summary[0]) if summary else "",
        }
    except etree.XMLSyntaxError as e:
        logger.warning("XML syntax error in %s: %s", path.name, e)
        return None
    except Exception as e:
        logger.warning("Error processing %s: %s", path.name, e)
        return None


def main() -> int:
    """Main entry point for letter parsing."""
    OUT_CSV.parent.mkdir(exist_ok=True)
    letters = [p for p in LETTERS.glob("*.xml") if p.name not in EXCLUDE]

    logger.info("Found %d letter files to process", len(letters))

    rows = []
    for p in letters:
        result = process_xml(p)
        if result:
            rows.append(result)

    rows.sort(key=lambda d: d["date"])

    with OUT_CSV.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "date",
                "place",
                "sender",
                "receiver",
                "repository",
                "idno",
                "locus",
                "word_count",
                "summary",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    logger.info("✅ Wrote %d rows to %s", len(rows), OUT_CSV)
    return 0


if __name__ == "__main__":
    sys.exit(main())
