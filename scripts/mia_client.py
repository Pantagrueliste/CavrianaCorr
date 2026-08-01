#!/usr/bin/env python3
"""A deliberately gentle client for the Medici Archive Project's MIA API.

The edition verifies its authority records against MAP. That is a small,
finite job: a few hundred lookups, once. This client is built so it cannot
accidentally become anything more.

  - Cache first. A response already on disk is never requested again, so
    re-running the enrichment costs zero requests.
  - One request at a time. No concurrency, ever. A fixed pause between calls
    keeps the rate near one request a second, well under what a person
    clicking through the interface produces in bursts.
  - A hard ceiling per run. If the budget is exhausted the run stops and
    tells you, rather than grinding on.
  - Backs off and gives up on 429 or 5xx instead of retrying into a wall.
  - Checkpoints after every call, so an interrupted run resumes instead of
    starting over.
  - Identifies itself, with a contact address. If this traffic ever puzzles
    anyone at MAP, they should be able to see whose it is and write to us.

The cache lives outside the published repository: it holds MAP's data, which
is theirs, not ours. Only the identifiers we cite end up in the TEI.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache" / "mia"
BASE = "https://mia.medici.org"

CONTACT = "cag437@nyu.edu"
USER_AGENT = f"CavrianaCorr-edition/1.0 (TEI edition of Cavriana's letters; {CONTACT})"

DELAY_SECONDS = 1.0      # pause between calls
MAX_CALLS_PER_RUN = 400  # hard ceiling; the whole job needs fewer


class Budget(Exception):
    """Raised when a run reaches its request ceiling."""


class Backoff(Exception):
    """Raised when the server signals it has had enough."""


class MiaClient:
    def __init__(self, cookie: str | None = None, delay: float = DELAY_SECONDS,
                 budget: int = MAX_CALLS_PER_RUN, dry_run: bool = False):
        self.cookie = cookie
        self.delay = delay
        self.budget = budget
        self.dry_run = dry_run
        self.calls = 0
        self.hits = 0
        CACHE.mkdir(parents=True, exist_ok=True)

    def _path(self, path: str) -> Path:
        safe = urllib.parse.quote(path, safe="")
        return CACHE / f"{safe}.json"

    def get(self, path: str) -> dict | None:
        """Fetch a MIA endpoint, or return the cached copy if we have one."""
        cached = self._path(path)
        if cached.exists():
            self.hits += 1
            return json.loads(cached.read_text(encoding="utf-8"))

        if self.dry_run:
            print(f"  would request {path}")
            return None
        if self.calls >= self.budget:
            raise Budget(f"stopped at the {self.budget}-request ceiling for this run")

        req = urllib.request.Request(BASE + path, headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            **({"Cookie": self.cookie} if self.cookie else {}),
        })
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                raise Backoff(f"server returned {e.code}; stopping rather than retrying") from e
            raise
        finally:
            self.calls += 1
            time.sleep(self.delay)          # pause even on failure

        data = json.loads(body)
        cached.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return data

    def report(self) -> str:
        return (f"{self.calls} request(s) made, {self.hits} served from cache "
                f"({self.budget - self.calls} left in this run's budget)")


if __name__ == "__main__":
    import sys
    c = MiaClient(dry_run="--dry-run" in sys.argv)
    print(f"cache: {CACHE}")
    print(f"cached responses on disk: {len(list(CACHE.glob('*.json')))}")
    print(c.report())
