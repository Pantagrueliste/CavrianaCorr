#!/usr/bin/env python3
"""Enforce the edition's line-break convention in the source files.

The rule, stated in the ODD as a Schematron constraint on <lb> and checked
here because nothing in the build runs Schematron yet:

  - a line break carries exactly one space before it and none after;
  - where a word runs on across the break, @break="no" and there is no space
    on either side, the hyphen being supplied on rendering;
  - the tagged line break is the only line break. The transcription stays on
    one line in the source, so that the shape of the page is carried by <lb>
    and never by the way the XML happens to be wrapped.

The last of these is the one that matters most. A newline in the middle of a
transcription is invisible in the reading text but competes with <lb> for the
same meaning, and whether it renders as a space or as nothing depends on
whitespace handling three steps away in the stylesheet.

Exit status is 1 if anything fails, so it can gate a build.
"""
from __future__ import annotations

import glob
import os
import sys

from lxml import etree

TEI = "{http://www.tei-c.org/ns/1.0}"


def local(tag) -> str:
    return tag.split("}")[-1] if isinstance(tag, str) else ""


def preceding_text(lb) -> str:
    """The text immediately before this line break, wherever it lives."""
    prev = lb.getprevious()
    return (prev.tail if prev is not None else lb.getparent().text) or ""


def check(path: str) -> list[str]:
    faults: list[str] = []
    body = etree.parse(path).getroot().find(f".//{TEI}body")
    if body is None:
        return faults
    name = os.path.basename(path)

    for lb in body.iter(TEI + "lb"):
        before = preceding_text(lb)
        after = lb.tail or ""
        # A run of line breaks is a blank line in the manuscript; the single
        # space between two of them is the second one's own space before.
        nxt = lb.getnext()
        next_is_lb = nxt is not None and local(nxt.tag) == "lb"

        if lb.get("break") == "no":
            if before.endswith((" ", "\t")):
                faults.append(f"{name}: space before <lb break=\"no\"/> — the word runs on")
            if after.startswith((" ", "\t")):
                faults.append(f"{name}: space after <lb break=\"no\"/> — the word runs on")
        else:
            if not before.endswith(" "):
                faults.append(f"{name}: <lb/> without the single space before it")
            elif before.endswith("  "):
                faults.append(f"{name}: more than one space before <lb/>")
            if after.startswith(" ") and not (next_is_lb and after == " "):
                faults.append(f"{name}: space after <lb/> — it belongs before the break")

    # No untagged line break anywhere a tagged one is in use.
    for holder in body.iter():
        if holder.find(TEI + "lb") is None:
            continue
        texts = [holder.text or ""]
        for d in holder.iter():
            if d is holder:
                continue
            texts.append(d.text or "")
            texts.append(d.tail or "")
        if any("\n" in t for t in texts):
            faults.append(
                f"{name}: a newline inside <{local(holder.tag)}> — the "
                f"transcription stays on one line"
            )
    return faults


def main() -> int:
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "letters")
    faults: list[str] = []
    files = sorted(glob.glob(os.path.join(root, "1*.xml")))
    for path in files:
        faults.extend(check(path))

    if faults:
        print(f"✗ {len(faults)} line-break faults in {len({f.split(':')[0] for f in faults})} letters\n")
        for f in faults[:40]:
            print("   " + f)
        if len(faults) > 40:
            print(f"   … and {len(faults) - 40} more")
        print("\nThe rule is in ODD_CavrianaCorr.xml, on <lb>.")
        return 1

    print(f"✓ {len(files)} letters keep the line-break convention")
    return 0


if __name__ == "__main__":
    sys.exit(main())
