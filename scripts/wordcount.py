#!/usr/bin/env python3
"""One definition of how many words a letter contains.

Two places needed this — the heatmap's daily figures and the edition's running
totals — and a count of the *text* is not a count of the *file*. What follows
is what a reader reads, and nothing else:

  - the body only, never the header, so a summary written by the editor is not
    counted as words Cavriana wrote;
  - the expansion of an abbreviation, not both forms. <choice> holds "V.S."
    and "Vostra Signoria" side by side, and counting the pair turns one word
    into three;
  - no ciphertext. A run of digits is not a word. Its decipherment is, and is
    counted;
  - no editorial note. A remark about the passage is not part of it. A
    marginal note is, being in the manuscript, and is counted;
  - no supplied gap. <gap/> stands for what cannot be read.

The count this replaces gathered p, div, opener and closer with one xpath, and
since div contains the others every word was counted twice; a letter of 431
words was reported as 862.
"""
from __future__ import annotations

import re

TEI = "{http://www.tei-c.org/ns/1.0}"


def _local(tag) -> str:
    return tag.split("}")[-1] if isinstance(tag, str) else ""


def _skip(el) -> bool:
    """Elements whose text is not part of the reading."""
    name = _local(el.tag)
    if name == "abbr":
        # only when there is an expansion to count instead
        parent = el.getparent()
        return parent is not None and parent.find(TEI + "expan") is not None
    if name == "seg" and el.get("type") == "cipher":
        return True
    if name == "note" and el.get("type") not in (None, "marginal"):
        return True
    return name == "gap"


def reading_text(body) -> str:
    """The letter as a reader meets it, with the encoding left behind."""
    if body is None:
        return ""
    out: list[str] = []

    def walk(el):
        if _skip(el):
            if el.tail:
                out.append(el.tail)
            return
        if el.text:
            out.append(el.text)
        for child in el:
            walk(child)
        if el.tail:
            out.append(el.tail)

    if body.text:
        out.append(body.text)
    for child in body:
        walk(child)
    return " ".join(out)


def count_words(body) -> int:
    text = re.sub(r"\s+", " ", reading_text(body)).strip()
    if not text:
        return 0
    # A word has a letter or a digit in it; bare punctuation does not count.
    return sum(1 for tok in text.split(" ") if re.search(r"[^\W_]", tok, re.UNICODE))
