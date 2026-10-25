# Pinned TEI validation inputs

The files in `tei-4.12.0/` are unmodified TEI Consortium P5 4.12.0
(revision `113e933e2`, 28 July 2026) distributions:

- `tei_all.rng`: https://www.tei-c.org/Vault/P5/4.12.0/xml/tei/custom/schema/relaxng/tei_all.rng
- `p5subset.xml`: https://www.tei-c.org/Vault/P5/4.12.0/xml/tei/odd/p5subset.xml

Copyright 2026 TEI Consortium. These files retain their upstream notices;
they are available under CC BY 3.0 or BSD-2-Clause, as described in their
headers (the full licence text is in `p5subset.xml`).

Both validation workflows use the local stock schema. `scripts/build_schema.py`
uses the local P5 source and pins the TEIC/Stylesheets processor to commit
`34da0f4c8f7d956fca3449dc7347181d034d0416`. This avoids depending on the TEI
website during CI and prevents upstream releases silently changing the rules.
The processor is still downloaded from GitHub on a cold cache.

When upgrading TEI, replace both files from the same release, update both
workflows and `build_schema.py`, regenerate the project schema, and validate
all `letters/*.xml` with Jing against both schemas. Also run
`python scripts/check_line_breaks.py`.

SHA-256 checksums:

```
5b89720edc6f3821ab3d0aa242aa5dc922bfbafabfb103d2de9d211001c33e26  p5subset.xml
b0f115095ead2ccc6933aa3365c6f4a82cba3b2ec7eee7f76bb616d7a63b7e48  tei_all.rng
```
