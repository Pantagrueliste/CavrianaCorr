# Python Scripts Documentation

This document describes the Python scripts used to process and visualize the Cavriana correspondence data.

## Prerequisites

Install dependencies:
```bash
pip install -r requirements.txt
```

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `letter_parser.py` | Parse XML letters and generate metadata CSV |
| `generate_heatmap.py` | Generate CalHeatmap React component |
| `generate_custom_heatmap.py` | Generate custom heatmap React component |
| `validate_references.py` | Validate entity references in letters |
| `update_heatmap.py` | Orchestrate heatmap generation + frontend sync |
| `update_custom_heatmap.py` | Orchestrate custom heatmap + frontend sync |
| `sync_frontend.py` | Copy generated files to frontend repo |

## Detailed Usage

### letter_parser.py

Parses all TEI-XML letter files and extracts metadata to a CSV file.

```bash
python scripts/letter_parser.py
```

**Input:** `letters/*.xml` (excludes `persNames.xml` and `placeNames.xml`)

**Output:** `data/letter_metadata.csv`

**CSV Columns:**
- `date` - Letter date (YYYY-MM-DD)
- `place` - Place of writing
- `sender` - Letter sender
- `receiver` - Letter recipient
- `repository` - Archive repository
- `idno` - Catalog/shelfmark ID
- `locus` - Folio location
- `word_count` - Number of words in letter body
- `summary` - Editorial summary

---

### generate_heatmap.py

Generates the CalHeatmap-based React component from template and CSV data.

```bash
python scripts/generate_heatmap.py
```

**Input:**
- `templates/CavrianaHeatmap.template.jsx`
- `data/letter_metadata.csv`

**Output:** `generated/CavrianaHeatmap.jsx`

---

### generate_custom_heatmap.py

Generates the custom heatmap React component.

```bash
python scripts/generate_custom_heatmap.py
```

**Input:**
- `templates/CustomHeatmap.template.jsx`
- `data/letter_metadata.csv`

**Output:** `generated/CustomHeatmap.jsx`

---

### validate_references.py

Validates that all entity references (`ref="#..."`) in letter files point to valid IDs in the authority files.

```bash
python scripts/validate_references.py
```

**Exit codes:**
- `0` - All references valid
- `1` - Missing references found

**Example output:**
```
Validating entity references...
Found 97 person IDs in persNames.xml
Found 72 place IDs in placeNames.xml
Checked 853 references across letter files
✓ All references are valid!
```

---

### update_heatmap.py

Master script that runs `generate_heatmap.py` followed by `sync_frontend.py`.

```bash
python scripts/update_heatmap.py
```

---

### update_custom_heatmap.py

Master script that runs `generate_custom_heatmap.py` followed by `sync_frontend.py --custom`.

```bash
python scripts/update_custom_heatmap.py
```

---

### sync_frontend.py

Copies generated heatmap files to the frontend repository.

```bash
# Sync CalHeatmap component
python scripts/sync_frontend.py

# Sync custom heatmap component
python scripts/sync_frontend.py --custom
```

**Note:** Requires `CavrianaCorr_FrontEnd` repository to be located at `../CavrianaCorr_FrontEnd/`

## Typical Workflow

1. Add/edit letter XML files in `letters/`
2. Run `python scripts/letter_parser.py` to regenerate CSV
3. Run `python scripts/generate_heatmap.py` to update visualization
4. Run `python scripts/validate_references.py` to check for broken refs

Or use the combined update scripts:
```bash
python scripts/update_heatmap.py
```

## Shared Utilities

The `heatmap_utils.py` module provides shared functions used by the heatmap generators:

- `setup_logging()` - Configure logging
- `load_metadata(csv_path)` - Load letter metadata from CSV
- `deduplicate_rows(rows)` - Handle duplicate dates
- `inject_years(template, years)` - Update YEARS constant in template
- `generate_heatmap(template_path, output_path)` - Main generation function
