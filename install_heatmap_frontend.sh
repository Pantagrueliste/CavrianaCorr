#!/bin/bash
# Installation script for Cavriana Heatmap component in the Docusaurus front-end

# Make this script executable: chmod +x install_heatmap_frontend.sh
# Usage: ./install_heatmap_frontend.sh /path/to/docusaurus/frontend

# Check if a directory path is provided
if [ $# -eq 0 ]
then
    echo "Error: No Docusaurus directory path provided"
    echo "Usage: $0 /path/to/docusaurus/frontend"
    exit 1
fi

DOCUSAURUS_DIR=$1

# Check if the Docusaurus directory exists
if [ ! -d "$DOCUSAURUS_DIR" ]
then
    echo "Error: Directory $DOCUSAURUS_DIR does not exist"
    exit 1
fi

# Create components directory if it doesn't exist
if [ ! -d "$DOCUSAURUS_DIR/src/components" ]
then
    echo "Creating components directory..."
    mkdir -p "$DOCUSAURUS_DIR/src/components"
    if [ $? -ne 0 ]
    then
        echo "Error: Failed to create components directory"
        exit 1
    fi
fi

# Create css directory if it doesn't exist
if [ ! -d "$DOCUSAURUS_DIR/src/css" ]
then
    echo "Creating css directory..."
    mkdir -p "$DOCUSAURUS_DIR/src/css"
    if [ $? -ne 0 ]
    then
        echo "Error: Failed to create css directory"
        exit 1
    fi
fi

# Copy the component to the Docusaurus components directory
echo "Copying component to $DOCUSAURUS_DIR/src/components/CavrianaHeatmap.jsx..."
cp CavrianaHeatmap.jsx "$DOCUSAURUS_DIR/src/components/"
if [ $? -ne 0 ]
then
    echo "Error: Failed to copy component"
    exit 1
fi

# Copy the CSS file to the Docusaurus css directory
echo "Copying CSS to $DOCUSAURUS_DIR/src/css/cavriana-heatmap.css..."
cp cavriana-heatmap.css "$DOCUSAURUS_DIR/src/css/"
if [ $? -ne 0 ]
then
    echo "Error: Failed to copy CSS file"
    exit 1
fi

# Update the CSS import in Docusaurus custom CSS file if exists
CUSTOM_CSS="$DOCUSAURUS_DIR/src/css/custom.css"
if [ -f "$CUSTOM_CSS" ]
then
    echo "Updating custom.css to import heatmap styles..."
    if ! grep -q "@import './cavriana-heatmap.css';" "$CUSTOM_CSS"
    then
        echo "" >> "$CUSTOM_CSS"
        echo "/* Cavriana Heatmap Styles */" >> "$CUSTOM_CSS"
        echo "@import './cavriana-heatmap.css';" >> "$CUSTOM_CSS"
    fi
else
    echo "Warning: custom.css not found, please manually import the CSS styles"
fi

# Add dependencies to package.json
echo "Installing required dependencies..."
cd "$DOCUSAURUS_DIR"
npm install --save cal-heatmap d3 @docusaurus/BrowserOnly

# Help message for integrating the component
echo ""
echo "==================================================================="
echo "Installation completed successfully!"
echo "==================================================================="
echo ""
echo "To add the heatmap to a Markdown page, include the following import at the top:"
echo ""
echo "import CavrianaHeatmap from '@site/src/components/CavrianaHeatmap';"
echo ""
echo "Then add the component in the content where you want it to appear:"
echo ""
echo "<CavrianaHeatmap />"
echo ""
echo "For example, to add it to intro.md, edit the file:"
echo "$DOCUSAURUS_DIR/docs/intro.md"
echo ""
echo "Start your Docusaurus development server to see the changes:"
echo "cd $DOCUSAURUS_DIR && npm start"
echo ""
echo "==================================================================="