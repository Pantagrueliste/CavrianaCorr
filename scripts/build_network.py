#!/usr/bin/env python3
"""Derive the network of people from the Medici Archive's document index.

Two people are connected when the same Medici Archive document names them
both. That is a fact about the archive, not a claim about acquaintance: most
of these ties are being written *about* together rather than writing to each
other, and the two are distinguished here.

What is published is the count, not the archive. The document identifiers and
titles that produced these numbers stay in the local cache, which is outside
this repository, because they are the Medici Archive Project's data and not
ours. What the edition publishes is its own derived measure over people it
already cites.

Input:  .cache/mia/network_edges.tsv   mapA <tab> mapB <tab> shared <tab> direct
Output: generated/network.json
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDGES = ROOT / ".cache" / "mia" / "network_edges.tsv"
AUTH = ROOT / "generated" / "authorities.json"
OUT = ROOT / "generated" / "network.json"

# Below this a shared document says little; it is as often an artefact of two
# people being mentioned in one long despatch as a relation worth drawing.
MIN_SHARED = 2


def main() -> None:
    if not EDGES.exists():
        raise SystemExit(f"no edge cache at {EDGES}; run the MAP sweep first")

    auth = json.loads(AUTH.read_text(encoding="utf-8"))
    people = {k: v for k, v in auth["entities"].items()
              if v["kind"] == "person" and not v.get("author")}
    by_map = {v["map"]: k for k, v in people.items() if v.get("map")}

    edges, skipped = [], 0
    for line in EDGES.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        a, b, n, direct = line.split("\t")
        pa, pb = by_map.get(a), by_map.get(b)
        if not pa or not pb:
            skipped += 1
            continue
        if int(n) < MIN_SHARED:
            continue
        edges.append({"a": pa, "b": pb, "shared": int(n), "direct": int(direct)})

    edges.sort(key=lambda e: -e["shared"])

    # A person's weight in the graph, and who they sit closest to.
    degree = defaultdict(int)
    for e in edges:
        degree[e["a"]] += e["shared"]
        degree[e["b"]] += e["shared"]

    neighbours = defaultdict(list)
    for e in edges:
        neighbours[e["a"]].append((e["shared"], e["direct"], e["b"]))
        neighbours[e["b"]].append((e["shared"], e["direct"], e["a"]))

    nodes = []
    for pid, rec in people.items():
        if pid not in degree:
            continue
        near = sorted(neighbours[pid], reverse=True)[:6]
        nodes.append({
            "id": pid,
            "name": rec["name"],
            "sortName": rec.get("sortName") or rec["name"],
            "map": rec.get("map", ""),
            "mentions": rec.get("total", 0),
            "degree": degree[pid],
            "nearest": [{"id": i, "shared": s, "direct": d} for s, d, i in near],
        })
    nodes.sort(key=lambda n: -n["degree"])

    OUT.write_text(json.dumps({
        "note": ("Derived from the Medici Archive Project's document index. An edge counts the "
                 "documents that name both people; 'direct' counts those where one is the sender "
                 "and the other the recipient. Document identifiers are not reproduced."),
        "minShared": MIN_SHARED,
        "nodes": nodes,
        "edges": edges,
    }, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    direct = sum(1 for e in edges if e["direct"])
    print(f"✅  {len(nodes)} people, {len(edges)} edges ({direct} with letters between them) → {OUT}")
    if skipped:
        print(f"    {skipped} edge(s) referenced a MAP id this edition does not cite")


if __name__ == "__main__":
    main()
