#!/usr/bin/env python3
"""Build the authority dataset the site uses for entity links and indexes.

Reads letters/persNames.xml, letters/placeNames.xml and every letter, and
writes generated/authorities.json: one record per person and place, plus the
list of letters that cite it. Consumed by the frontend's Ent component and
by the people/places index pages.
"""
from __future__ import annotations

import csv
import json
from datetime import date, timedelta
import re
from collections import defaultdict
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parent.parent
LETTERS = ROOT / "letters"
OUT = ROOT / "generated" / "authorities.json"
CSV = ROOT / "generated" / "authorities.csv"

NS = {"tei": "http://www.tei-c.org/ns/1.0"}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
# A letter is a document with a correspondence action. Authority files have
# none, so they exclude themselves and new ones need no maintenance here.
def is_letter(root) -> bool:
    return bool(root.xpath(".//tei:correspAction", namespaces=NS))


def text(el) -> str:
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip() if el is not None else ""


def reckoned(el, attr: str) -> str:
    """The value of a date attribute in the edition's own reckoning.

    In TEI @when is Gregorian by definition, so a Julian date belongs in
    @when-custom with @datingMethod naming the calendar. This edition works in
    the Julian reckoning the letters themselves use — Coligny dies on Saint
    Bartholomew's day, not ten days after it — so the custom value wins where
    there is one.
    """
    return el.get(attr + "-custom") or el.get(attr) or ""


def date_of(el) -> str:
    """A date element may carry its value as text, as @when, or as a range."""
    if el is None:
        return ""
    return (text(el) or reckoned(el, "when") or reckoned(el, "from")
            or reckoned(el, "notBefore") or "")


def map_footprint() -> dict:
    """How each person figures in the Medici Archive as a whole.

    Counts only: how many documents name them, and in what capacity. The
    documents themselves are MAP's, and stay in the local cache.
    """
    path = ROOT / "sources" / "map" / "footprint.tsv"
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        mid, total, sent, received, named = line.split("\t")
        if int(total) == 0:
            continue
        out[mid] = {"documents": int(total), "sent": int(sent),
                    "received": int(received), "named": int(named)}
    return out


def map_categories() -> dict:
    """The Medici Archive's own classification of each person's offices.

    Its value here is as a finding aid: it lets a reader ask the index for the
    churchmen, or the soldiers, across a hundred and ten people.
    """
    path = ROOT / "sources" / "map" / "categories.tsv"
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        mid, cats = line.split("\t")
        out[mid] = [c for c in cats.split("|") if c]
    return out


def calling(cats: list, offices: list) -> str:
    """One calling per person, for narrowing the index.

    MAP assigns several overlapping categories to most people, and two of them
    are no use here. "Nobility" covers more than half the list and so
    distinguishes nobody. "Corporate bodies" classifies an office by the
    institution it sits in, not the person holding it — it is why a Medici
    secretary came out labelled a corporation.

    A calling is claimed only where there is evidence for it: MAP tags the Duke
    of Guise "state and court" from a title rather than a post, and he holds no
    recorded office, so he is left uncalled rather than filed as an official.
    """
    if "Church" in cats:
        return "Church"
    if "Heads of state" in cats:
        return "Rulers"
    if "Military" in cats:
        return "Military"
    if "State and court" in cats and offices:
        return "Officials and envoys"
    return ""


def build_persons() -> dict:
    doc = etree.parse(str(LETTERS / "persNames.xml"))
    footprint = map_footprint()
    categories = map_categories()
    out = {}
    for p in doc.xpath(".//tei:person", namespaces=NS):
        pid = p.get(XML_ID)
        if not pid:
            continue
        names = p.xpath("./tei:persName", namespaces=NS)
        primary = next((n for n in names if n.get("type") not in ("alias", "sort")), None)
        # An alias the edition vouches for, and one it only proposes, are not
        # the same claim. "Messer Alberto segretario" is probably Alberto
        # Luchi; the index must say probably, not "also called".
        aliases = [text(n) for n in names
                   if n.get("type") == "alias" and not n.get("cert")]
        proposed = [text(n) for n in names
                    if n.get("type") == "alias" and n.get("cert")]
        sort_form = next((text(n) for n in names if n.get("type") == "sort"), "")
        occs = p.xpath("./tei:occupation", namespaces=NS)
        occ = occs[0] if occs else None
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
            "probableName": next((p for p in proposed if p), ""),
            "role": text(occ),
            "roleType": occ.get("type", "") if occ is not None else "",
            # Further offices, mostly from the Medici Archive's own records.
            # Dated ones let the edition say what a man held when a letter names him.
            "offices": [
                {"label": text(o), "from": o.get("from", ""), "to": o.get("to", "")}
                for o in occs[1:]
            ],
            "roleFrom": occ.get("from", "") if occ is not None else "",
            "roleTo": occ.get("to", "") if occ is not None else "",
            "birth": date_of(p.find("tei:birth", NS)),
            "death": date_of(p.find("tei:death", NS)),
            # The plain note describes the person. Typed notes record editorial
            # matter — a disputed date, a rejected identification — and belong
            # in the file, not on a card beside a sentence.
            "note": next((text(n) for n in p.xpath("./tei:note[not(@type)]", namespaces=NS)), ""),
            "viaf": viaf.strip(),
            "map": idnos.get("MAP", ""),
            "dbi": idnos.get("DBI", ""),
            # the person's presence in the Medici Archive at large
            "archive": footprint.get(idnos.get("MAP", ""), None),
            "calling": calling(categories.get(idnos.get("MAP", ""), []), occs[1:]),
            "wikidata": idnos.get("WIKIDATA", ""),
            # Commons file name; the image itself stays on Commons.
            "image": idnos.get("WIKIMEDIA_IMAGE", ""),
        }
    return out


# A people standing for a country is also a group. These have no record of
# their own: the place carries the count, and the group list borrows it, so
# "i Corsi" is not counted twice.
ETHNIC_GROUPS = {
    "place-fr": ("grp-french", "French"),
    "place-it": ("grp-italians", "Italians"),
    "place-es": ("grp-spanish", "Spanish"),
    "place-england": ("grp-english", "English"),
    "place-svizzera": ("grp-swiss", "Swiss"),
    "place-ottoman": ("grp-turks", "Turks"),
    "place-corsica": ("grp-corsicans", "Corsicans"),
    "place-de": ("grp-germans", "Germans"),
}


def build_groups() -> dict:
    """The collectives Cavriana writes about, as against the individuals."""
    path = LETTERS / "groupNames.xml"
    if not path.exists():
        return {}
    doc = etree.parse(str(path))
    out = {}
    for g in doc.xpath(".//tei:personGrp", namespaces=NS):
        gid = g.get(XML_ID)
        if not gid:
            continue
        names = g.xpath("./tei:persName", namespaces=NS)
        primary = next((n for n in names if n.get("type") not in ("alias", "sort")), None)
        idnos = {i.get("type"): text(i) for i in g.xpath("./tei:idno", namespaces=NS)}
        out[gid] = {
            "kind": "group",
            "name": text(primary) if primary is not None else gid,
            "sortName": next((text(n) for n in names if n.get("type") == "sort"), "")
                        or (text(primary) if primary is not None else gid),
            "aliases": [text(n) for n in names if n.get("type") == "alias"],
            "role": g.get("role", ""),
            "note": text(g.find("tei:note", NS)),
            "wikidata": idnos.get("WIKIDATA", ""),
            "place": "",
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


def build_events() -> list:
    """Public events, with the letters written around them.

    Letters are attached by date, which is a fact about when they were written,
    not a claim that they discuss the event. Dates on both sides are Julian.
    """
    path = LETTERS / "eventNames.xml"
    if not path.exists():
        return []
    doc = etree.parse(str(path))
    out = []
    for ev in doc.xpath(".//tei:event", namespaces=NS):
        labels = [text(l) for l in ev.xpath("./tei:label", namespaces=NS)]
        idnos = {i.get("type"): text(i) for i in ev.xpath("./tei:idno", namespaces=NS)}
        out.append({
            "id": ev.get(XML_ID),
            "label": labels[0] if labels else ev.get(XML_ID),
            "labels": labels,
            "desc": text(ev.find("tei:desc", NS)),
            "when": reckoned(ev, "when"),
            "from": reckoned(ev, "from"),
            "to": reckoned(ev, "to"),
            "wikidata": idnos.get("WIKIDATA", ""),
        })
    return out


def attach_letters(events: list, dates: dict) -> None:
    """For each event, the letters written around it."""
    def d(s):
        try:
            return date.fromisoformat(s)
        except (ValueError, TypeError):
            return None
    known = sorted(((d(v), k) for k, v in dates.items() if d(v)))
    for ev in events:
        start = d(ev["from"] or ev["when"])
        end = d(ev["to"] or ev["when"])
        if not start:
            ev["letters"] = []
            continue
        lo, hi = start - timedelta(days=21), end + timedelta(days=45)
        near = [(dt, slug) for dt, slug in known if lo <= dt <= hi]
        ev["letters"] = [{
            "slug": slug,
            "date": dt.isoformat(),
            "days": (dt - start).days,
        } for dt, slug in near]
        after = [l for l in ev["letters"] if l["days"] >= 0]
        ev["firstAfter"] = after[0]["slug"] if after else ""


def collect_occurrences() -> tuple[dict, dict]:
    """Map authority id -> [{file, date, count}], counting body references only.

    Returns place/person references, references by people-name, and letter dates.
    """
    occ = defaultdict(lambda: defaultdict(int))
    eth = defaultdict(lambda: defaultdict(int))
    dates = {}
    published = set()
    for f in sorted(LETTERS.glob("*.xml")):
        root = etree.parse(str(f)).getroot()
        if not is_letter(root):
            continue
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
        # A people named for their country counts towards the place, but is
        # counted apart: naming Frenchmen is not naming France.
        for el in root.xpath(".//tei:text//tei:rs[@type='ethnic'][@ref]", namespaces=NS):
            ref = (el.get("ref") or "").lstrip("#")
            if ref:
                eth[ref][slug] += 1
        for el in root.xpath(".//tei:text//tei:rs[@type='group'][@ref]", namespaces=NS):
            ref = (el.get("ref") or "").lstrip("#")
            if ref:
                occ[ref][slug] += 1
    return occ, eth, dates


def write_csv(entities: dict) -> None:
    """A flat table of the reconciliation, for anyone who wants the identifiers.

    This edition checked every one of these against the authority itself, and
    found the identifiers it inherited to be largely wrong. Publishing the
    corrected set as a plain table costs nothing and saves the next person the
    same work — including, where they are missing upstream, the Medici Archive
    identifiers.
    """
    cols = ["id", "kind", "name", "sortName", "birth", "death",
            "viaf", "wikidata", "map", "dbi", "tgn", "geonames",
            "lat", "lon", "mentions", "letters"]
    rows = []
    for eid, r in sorted(entities.items()):
        rows.append({
            "id": eid,
            "kind": r["kind"],
            "name": r.get("name", ""),
            "sortName": r.get("sortName", ""),
            "birth": r.get("birth", ""),
            "death": r.get("death", ""),
            "viaf": r.get("viaf", ""),
            "wikidata": r.get("wikidata", ""),
            "map": r.get("map", ""),
            "dbi": r.get("dbi", ""),
            "tgn": r.get("tgn", ""),
            "geonames": r.get("geonames", ""),
            "lat": r.get("lat", ""),
            "lon": r.get("lon", ""),
            "mentions": r.get("total", 0),
            "letters": len(r.get("letters", [])),
        })
    with CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    persons, places, groups = build_persons(), build_places(), build_groups()
    occ, eth, dates = collect_occurrences()
    events = build_events()
    attach_letters(events, dates)

    # Peoples that stand for a country become groups too, borrowing the place's
    # own tally rather than being counted again.
    for pid, (gid, label) in ETHNIC_GROUPS.items():
        rec = places.get(pid)
        if not rec or not eth.get(pid):
            continue
        groups[gid] = {
            "kind": "group", "name": label, "sortName": label, "aliases": [],
            "role": "people", "note": "", "wikidata": rec.get("wikidata", ""),
            "place": pid,
        }
        occ[gid] = dict(eth[pid])

    entities = {**persons, **places, **groups}
    for eid, rec in entities.items():
        letters = [{"slug": s, "date": dates.get(s, ""), "n": n}
                   for s, n in sorted(occ.get(eid, {}).items())]
        rec["letters"] = letters
        rec["total"] = sum(l["n"] for l in letters)
        peoples = [{"slug": s, "date": dates.get(s, ""), "n": n}
                   for s, n in sorted(eth.get(eid, {}).items())]
        if peoples:
            rec["asPeople"] = peoples
            rec["asPeopleTotal"] = sum(l["n"] for l in peoples)

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({
        "entities": entities,
        "events": events,
        "dates": dates,
    }, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    write_csv(entities)

    cited = sum(1 for r in entities.values() if r["total"])
    print(f"✅  wrote {len(entities)} authority records "
          f"({cited} cited, {len(entities) - cited} never cited) "
          f"and {len(events)} events → {OUT}")
    print(f"    flat table of identifiers → {CSV}")


if __name__ == "__main__":
    main()
