# Cavriana Correspondence Heatmap

This tool generates a GitHub-style calendar heatmap visualization of Filippo Cavriana's letter-writing activity over time, based on word counts from the TEI-encoded letters in the repository.

## Features

- Shows a calendar heatmap of letter writing activity
- Color intensity represents the amount of text (word count) written on each day
- Automatically updates when new letters are added to the repository
- Seamlessly integrates with Docusaurus

## How It Works

1. The `letter_parser.py` script processes all TEI XML files in the `letters/` directory and extracts metadata including dates and word counts.
2. The `cavriana_heatmap.py` script generates a React component for Docusaurus that creates an interactive calendar heatmap.
3. A GitHub Actions workflow automatically updates the heatmap component in the Docusaurus frontend repository whenever new letters are added.

## Manual Update Process

You can manually update the heatmap by running:

```bash
python letter_parser.py  # Generate letter_metadata.csv from XML files
python cavriana_heatmap.py  # Generate the heatmap component
```

This will create a file called `CavrianaHeatmap.jsx` that can be copied to your Docusaurus project.

## Integration with Docusaurus

### Dependencies

Add these dependencies to your Docusaurus project:

```bash
npm install cal-heatmap d3 @docusaurus/BrowserOnly
```

### Usage in Docusaurus

1. Copy the generated `CavrianaHeatmap.jsx` to your Docusaurus project's `src/components/` directory.
2. Import and use the component in your Markdown files:

```md
import CavrianaHeatmap from '@site/src/components/CavrianaHeatmap';

# Filippo Cavriana's Correspondence

<CavrianaHeatmap />

Regular markdown content continues here...
```

### Styling

You can add custom CSS for the heatmap in your Docusaurus CSS files:

```css
.cavriana-heatmap {
  margin: 2rem 0;
}

.cavriana-heatmap .legend {
  display: flex;
  align-items: center;
  margin-top: 1rem;
}

.cavriana-heatmap .legend-title {
  margin-right: 1rem;
  font-weight: bold;
}

.cavriana-heatmap .legend-scale {
  display: inline-block;
  width: 150px;
  height: 20px;
  background: linear-gradient(to right, #f7fcf0, #41ab5d);
  margin: 0 10px;
}

.cavriana-heatmap .note {
  font-size: 0.8rem;
  color: #666;
  margin-top: 1rem;
}
```

## GitHub Actions Workflow

The included GitHub Actions workflow will automatically:

1. Run whenever new letters are added to the `letters/` directory
2. Generate updated letter metadata and the heatmap component
3. Push the changes to your Docusaurus frontend repository

Note: You'll need to add a repository secret named `FRONTEND_REPO_TOKEN` containing a GitHub Personal Access Token with write access to your Docusaurus repository.