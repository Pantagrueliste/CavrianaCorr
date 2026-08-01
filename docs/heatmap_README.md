# Letter Heatmap: Generation and Synchronization

The site's calendar heatmap is a GitHub-style activity visualization of
Cavriana's letter-writing, built with pure React and SVG (no external
charting libraries). Colour intensity represents text volume (word count).

## How it works

The pipeline runs automatically in CI
(`.github/workflows/update-heatmap.yml`) on every push that touches
`letters/`, `scripts/`, the component template, or the heatmap stylesheet:

1. `scripts/letter_parser.py` extracts metadata from every letter in
   `letters/` into `data/letter_metadata.csv` (one row per TEI file, keyed
   by the `file` column). Letters whose sent date has only a
   `notBefore`/`notAfter` range register under their `notBefore` date.
2. `scripts/generate_custom_heatmap.py` injects the CSV data into
   `templates/CustomHeatmap.template.jsx` and writes
   `generated/CustomHeatmap.jsx`.
3. CI copies `generated/CustomHeatmap.jsx` to the frontend's
   `src/components/` and `assets/cavriana-heatmap-custom.css` to the
   frontend's `src/css/`, smoke-builds the site, and pushes.

To run the generation locally:

```bash
# from the CavrianaCorr directory
python scripts/letter_parser.py
python scripts/generate_custom_heatmap.py
```

## Files

- **`templates/CustomHeatmap.template.jsx`** — component template with a
  data placeholder.
- **`generated/CustomHeatmap.jsx`** — generated component (do not edit by
  hand; regenerate instead).
- **`assets/cavriana-heatmap-custom.css`** — heatmap styles, including
  dark-mode rules.
- **`scripts/letter_parser.py`** — CSV extraction.
- **`scripts/generate_custom_heatmap.py`** — component generation.

## Component features

- Pure SVG rendering (day cells as `<rect>`s), no runtime dependencies.
- Year navigation via buttons and prev/next controls.
- Tooltips with per-day letter details.
- Colour-scale legend.
- Responsive layout and Docusaurus light/dark theme support.

## Usage in the frontend

`docs/intro.md` in the frontend imports the component:

```jsx
import CustomHeatmap from '@site/src/components/CustomHeatmap';

<CustomHeatmap />
```

The stylesheet is loaded globally via the `customCss` array in
`docusaurus.config.js`.
