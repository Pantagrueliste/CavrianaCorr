# Derived from the Medici Archive Project

Two small tables, both counts and classifications rather than content.

- `footprint.tsv` — for each person this edition cites and has matched to MAP:
  the number of documents in the Medici Archive that name them, and how many
  of those they sent, received, or are merely named in.
  Columns: `mapId  documents  sent  received  named`.

- `categories.tsv` — the categories MAP assigns to the offices a person held,
  used to let the index be narrowed to the churchmen, the soldiers and so on.
  Columns: `mapId  category|category`.

They are tracked here rather than left in the local cache because the site is
built from them in CI, where the cache does not exist. MAP's document
identifiers, titles and summaries are *not* here: those are the Medici Archive
Project's material and stay in `.cache/`, outside the repository.
