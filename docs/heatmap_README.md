# Cavriana Heatmap Generation and Synchronization

This documentation explains how to use the scripts that generate and maintain the GitHub-style heatmap showing Cavriana's letter-writing activity.

## Overview

The heatmap visualization is generated from CSV metadata in `data/letter_metadata.csv` and displayed in the Docusaurus frontend. The system consists of:

1. A CSV file containing letter metadata (date, word count, etc.)
2. A template JSX component for the heatmap
3. A Python script to generate the heatmap component
4. A synchronization script to copy the component to the frontend
5. The React component in the frontend that renders the heatmap

## Scripts

### `update_heatmap.py`

This is the main script you should use to update the heatmap. It:

1. Generates the heatmap component from the CSV data
2. Synchronizes the generated component with the frontend

```bash
# Run from the CavrianaCorr directory
python scripts/update_heatmap.py
```

### `generate_heatmap.py`

This script reads the letter metadata CSV and generates a React component file in `generated/CavrianaHeatmap.jsx`.

```bash
# Run from the CavrianaCorr directory
python scripts/generate_heatmap.py
```

### `sync_frontend.py`

This script copies the generated heatmap component to the frontend repository.

```bash
# Run from the CavrianaCorr directory
python scripts/sync_frontend.py
```

## Workflow

1. Update letter metadata in `data/letter_metadata.csv`
2. Run `python scripts/update_heatmap.py` to update the heatmap
3. In the frontend directory, run `npm start` to preview the changes
4. Commit and push changes in both repositories

## Troubleshooting

If the heatmap doesn't display correctly:

1. Check that the CSV has valid data with `date` and `word_count` columns
2. Verify that the generated component was correctly copied to the frontend
3. Make sure the frontend is using the correct CSS for the heatmap
4. Check the browser console for any JavaScript errors

## CSS Styling

The heatmap styling is defined in `assets/cavriana-heatmap.css` and copied to the frontend during synchronization. If you need to adjust the heatmap appearance, modify this file and run the update script again.

## Handling Duplicate Dates

When multiple letters exist for the same date, the system will now use the maximum word count value for that date to ensure consistent display. This resolves the issue with entries like "1570-07-29" appearing in different orders.

## Plugin Configuration

The heatmap uses the `LegendLite` and `Tooltip` plugins from cal-heatmap. If you need to modify how these plugins work:

1. Update the template in `templates/CavrianaHeatmap.template.jsx`
2. Run the update script to propagate changes to the frontend