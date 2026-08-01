#!/usr/bin/env python3
"""Build the authority dataset the site uses for entity links and indexes.

Reads letters/persNames.xml, letters/placeNames.xml and every letter, and
writes generated/authorities.json: one record per person and place, plus the
list of letters that cite it. Consumed by the frontend's Ent component and
by the people/places index pages.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parent.parent
LETTERS = ROOT / "letters"
OUT = ROOT / "generated" / "authorities.json"

NS = {"tei": "http://www.tei-c.org/ns/1.0"}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
EXCLUDE = {"persNames.xml", "placeNames.xml"}


def text(el) -> str:
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip() if el is not None else ""


def build_persons() -> dict:
    doc = etree.parse(str(LETTERS / "persNames.xml"))
    out = {}
    for p in doc.xpath(".//tei:person", namespaces=NS):
        pid = p.get(XML_ID)
        if not pid:
            continue
        names = p.xpath("./tei:persName", namespaces=NS)
        primary = next((n for n in names if n.get("type") not in ("alias", "sort")), None)
        aliases = [text(n) for n in names if n.get("type") == "alias"]
        sort_form = next((text(n) for n in names if n.get("type") == "sort"), "")
        occ = p.find("tei:occupation", NS)
        idnos = {i.get("type"): text(i) for i in p.xpath("./tei:idno", namespaces=NS)}
        viaf = idnos.get("VIAF", "")
        out[pid] = {
            "kind": "person",
            # The correspondence's own author, who signs nearly every letter,
            # is recorded here but not listed among the people it names.
            "author": p.get("role") == "author",
            "name": text(primary) if primary is not None else pid,
            # Index form, family name first; falls back to natural order.
            "sortName": sort_form or (text(primary) if primary is not None else pid),
            "aliases": [a for a in aliases if a],
            "role": text(occ),
            "roleType": occ.get("type", "") if occ is not None else "",
            "birth": text(p.find("tei:birth", NS)),
            "death": text(p.find("tei:death", NS)),
            "note": text(p.find("tei:note", NS)),
            "viaf": viaf.strip(),
            "map": idnos.get("MAP", ""),
            "wikidata": idnos.get("WIKIDATA", ""),
            # Commons file name; the image itself stays on Commons.
            "image": idnos.get("WIKIMEDIA_IMAGE", ""),
        }
    return out


def build_places() -> dict:
    doc = etree.parse(str(LETTERS / "placeNames.xml"))
    out = {}
    for pl in doc.xpath(".//tei:place", namespaces=NS):
        pid = pl.get(XML_ID)
        if not pid:
            continue
        names = pl.xpath("./tei:placeName", namespaces=NS)
        by_type = defaultdict(list)
        for n in names:
            by_type[n.get("type", "other")].append(text(n))
        geo = text(pl.find(".//tei:geo", NS))
        lat, lon = "", ""
        if geo:
            parts = geo.replace(",", " ").split()
            if len(parts) >= 2:
                lat, lon = parts[0], parts[1]
        idnos = {i.get("type"): text(i) for i in pl.xpath("./tei:idno", namespaces=NS)}
        tgn = idnos.get("TGN", "")
        modern = by_type.get("modern", [])
        historical = by_type.get("historical", [])
        # Some records carry a single untyped placeName, which is the name.
        untyped = by_type.get("other", [])
        out[pid] = {
            "kind": "place",
            # country and continent records name a whole polity, not a point
            "scope": pl.get("type", ""),
            "name": (modern or untyped or historical or [pid])[0],
            "sortName": (modern or untyped or historical or [pid])[0],
            "historical": historical,
            "country": (by_type.get("country") or [""])[0],
            "lat": lat,
            "lon": lon,
            "tgn": tgn.rsplit("/", 1)[-1] if tgn else "",
            "wikidata": idnos.get("WIKIDATA", ""),
            "geonames": idnos.get("GEONAMES", ""),
            "note": text(pl.find("tei:note", NS)),
        }
    return out


def collect_occurrences() -> tuple[dict, dict]:
    """Map authority id -> [{file, date, count}], counting body references only."""
    occ = defaultdict(lambda: defaultdict(int))
    dates = {}
    published = set()
    for f in sorted(LETTERS.glob("*.xml")):
        if f.name in EXCLUDE:
            continue
        root = etree.parse(str(f)).getroot()
        if root.xpath(".//tei:revisionDesc[@status='placeholder']", namespaces=NS):
            continue
        slug = f.stem
        published.add(slug)
        d = root.xpath(".//tei:correspAction[@type='sent']/tei:date", namespaces=NS)
        dates[slug] = (d[0].get("when") or d[0].get("notBefore") or "") if d else ""
        for el in root.xpath(".//tei:text//tei:persName[@ref] | .//tei:text//tei:placeName[@ref]",
                             namespaces=NS):
            ref = (el.get("ref") or "").lstrip("#")
            if ref:
                occ[ref][slug] += 1
    return occ, dates


def main() -> None:
    persons, places = build_persons(), build_places()
    occ, dates = collect_occurrences()

    entities = {**persons, **places}
    for eid, rec in entities.items():
        letters = [{"slug": s, "date": dates.get(s, ""), "n": n}
                   for s, n in sorted(occ.get(eid, {}).items())]
        rec["letters"] = letters
        rec["total"] = sum(l["n"] for l in letters)

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({
        "entities": entities,
        "dates": dates,
    }, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    cited = sum(1 for r in entities.values() if r["total"])
    print(f"✅  wrote {len(entities)} authority records "
          f"({cited} cited, {len(entities) - cited} never cited) → {OUT}")


if __name__ == "__main__":
    main()
