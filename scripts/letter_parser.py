#!/usr/bin/env python3
import re, csv
from pathlib import Path
from datetime import datetime
from lxml import etree

# ── locate repo root ────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent   # …/CavrianaCorr
OUT_CSV   = REPO_ROOT / "data"    / "letter_metadata.csv"
LETTERS   = REPO_ROOT / "letters"                     # XML folder
# ────────────────────────────────────────────────────────────────────────

EXCLUDE = {"persNames.xml", "placeNames.xml"}
NS      = {"tei": "http://www.tei-c.org/ns/1.0"}

def count_words(text: str) -> int:
    return len(re.sub(r"\s+", " ", text).strip().split())

def get_text(elem):
    if elem is None:
        return ""
    txt = elem.text or ""
    for child in elem:
        txt += " " + get_text(child)
    if elem.tail:
        txt += " " + elem.tail
    return txt.strip()

def count_body_words(body_elem):
    txt = " ".join(
        get_text(e) for e in body_elem.xpath(
            ".//tei:p | .//tei:div | .//tei:opener | .//tei:closer",
            namespaces=NS,
        )
    )
    return count_words(txt)

def process_xml(path: Path):
    try:
        root = etree.parse(path).getroot()
        q = lambda xp: root.xpath(xp, namespaces=NS)

        date  = q("//tei:correspAction[@type='sent']/tei:date")
        place = q("//tei:correspAction[@type='sent']/tei:placeName")
        sender   = q("//tei:correspAction[@type='sent']/tei:persName")
        receiver = q("//tei:correspAction[@type='received']/tei:persName")
        repo  = q("//tei:msIdentifier/tei:repository")
        idno  = q("//tei:msIdentifier/tei:idno")
        locus_elem = q("//tei:msItem/tei:locus")
        summary    = q("//tei:note[@type='summary']")
        body       = q("//tei:text/tei:body")

        locus = ""
        if locus_elem:
            fr, to = locus_elem[0].get("from"), locus_elem[0].get("to")
            locus  = f"{fr}-{to}" if fr and to else get_text(locus_elem[0])

        word_count = count_body_words(body[0]) if body else 0

        return {
            "date"      : date[0].get("when") if date else "",
            "place"     : get_text(place[0])   if place else "",
            "sender"    : get_text(sender[0])  if sender else "",
            "receiver"  : get_text(receiver[0])if receiver else "",
            "repository": get_text(repo[0])    if repo else "",
            "idno"      : get_text(idno[0])    if idno else "",
            "locus"     : locus,
            "word_count": word_count,
            "summary"   : get_text(summary[0]) if summary else "",
        }
    except Exception as e:
        print(f"⚠️  {path.name}: {e}")
        return None

def main():
    OUT_CSV.parent.mkdir(exist_ok=True)          # create data/
    letters = [p for p in LETTERS.glob("*.xml") if p.name not in EXCLUDE]

    rows = [r for p in letters if (r := process_xml(p))]
    rows.sort(key=lambda d: d["date"])

    with OUT_CSV.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "date","place","sender","receiver","repository",
                "idno","locus","word_count","summary"
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅  wrote {len(rows)} rows → {OUT_CSV}")

if __name__ == "__main__":
    main()