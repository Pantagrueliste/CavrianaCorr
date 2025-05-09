# Custom Heatmap Implementation

This document explains the custom React-based heatmap implementation that replaces the previous CalHeatmap version.

## Overview

The custom heatmap provides a GitHub-style activity visualization for Cavriana's letter-writing activity. It is built using pure React and SVG, eliminating the dependency on external libraries like CalHeatmap and D3.js.

## Key Features

- **Pure SVG Rendering**: The heatmap is rendered using SVG rectangles for day cells, providing better control over the rendering process.
- **Year Navigation**: Users can navigate between years using year buttons or prev/next navigation.
- **Tooltip Support**: Hovering over a day cell shows detailed information about that day's activity.
- **Color Scale Legend**: A legend shows the color scale used to represent activity levels.
- **Responsive Design**: The heatmap adapts to different screen sizes.
- **Light/Dark Mode Support**: Uses Docusaurus theme variables for consistent appearance in light and dark modes.
- **Complete Re-rendering Between Years**: Uses React's key prop to ensure the grid completely re-renders when switching years.

## Files Structure

- **`templates/CustomHeatmap.template.jsx`**: Template for the React component, with a placeholder for data.
- **`generated/CustomHeatmap.jsx`**: The generated component with actual data (created by the generation script).
- **`assets/cavriana-heatmap-custom.css`**: CSS styles for the custom heatmap.
- **`scripts/generate_custom_heatmap.py`**: Script to generate the component from the template and data.
- **`scripts/update_custom_heatmap.py`**: Script to generate and sync the custom heatmap to the frontend.

## Usage in Docusaurus

To use the custom heatmap in your Docusaurus site:

1. Import the component and CSS in your page:

```jsx
import CustomHeatmap from '@site/src/components/CustomHeatmap';
import '@site/src/css/cavriana-heatmap-custom.css';

// In your React component:
<CustomHeatmap />
```

## Updating the Heatmap

When you need to update the heatmap (e.g., after adding new letter data):

1. Update the letter metadata in `data/letter_metadata.csv`.
2. Run the update script:

```bash
python scripts/update_custom_heatmap.py
```

This will generate the new component and sync it to the frontend.

## Migrating from CalHeatmap

If you are migrating from the previous CalHeatmap implementation:

1. Update your imports to use the custom component:
   ```diff
   - import CavrianaHeatmap from '@site/src/components/CavrianaHeatmap';
   - import '@site/src/css/cavriana-heatmap.css';
   + import CustomHeatmap from '@site/src/components/CustomHeatmap';
   + import '@site/src/css/cavriana-heatmap-custom.css';
   ```

2. Update your component usage:
   ```diff
   - <CavrianaHeatmap />
   + <CustomHeatmap />
   ```

3. Remove CalHeatmap and D3.js dependencies from your project:
   ```bash
   npm uninstall cal-heatmap d3
   ```

4. Run the cleanup script to backup and identify legacy files:
   ```bash
   python scripts/clean_legacy_heatmap.py
   ```

## Customization

The appearance of the heatmap can be customized by modifying:

- **`templates/CustomHeatmap.template.jsx`**: For behavioral changes and the default color scale.
- **`assets/cavriana-heatmap-custom.css`**: For styling changes.

After making changes, run the update script to regenerate and sync the component.

## Troubleshooting

If the heatmap doesn't display correctly:

1. Check that the component is properly imported and the CSS is loaded.
2. Verify that the data is correctly formatted in the CSV file.
3. Check browser console for any JavaScript errors.
4. Ensure that the component was successfully generated and synced to the frontend.