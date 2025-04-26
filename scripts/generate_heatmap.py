import pandas as pd
import numpy as np
import os
import csv
from datetime import datetime, timedelta
import json

def create_heatmap_data():
    """
    Process the letter metadata CSV and create data for a calendar heatmap
    """
    # Read the CSV file
    try:
        df = pd.read_csv('letter_metadata.csv')
    except FileNotFoundError:
        print("Error: letter_metadata.csv not found. Run letter_parser.py first.")
        return None
    
    # Handle the historical dates properly
    # Instead of using pandas timestamp which has limits, 
    # we'll manually convert YYYY-MM-DD strings to JavaScript timestamps
    heatmap_data = {}
    
    for _, row in df.iterrows():
        try:
            # Parse the date string (format: YYYY-MM-DD)
            date_parts = row['date'].split('-')
            year = int(date_parts[0])
            month = int(date_parts[1]) - 1  # JavaScript months are 0-indexed
            day = int(date_parts[2])
            
            # Create a date string in a format JavaScript can understand
            # Format: milliseconds since Jan 1, 1970
            # For historical dates, we'll use the JS timestamp calculation formula
            js_timestamp = int(datetime(year, month+1, day).timestamp()) * 1000
            
            # Store the word count for this date
            word_count = int(row['word_count'])
            
            # Add to our heatmap data (convert to seconds for cal-heatmap)
            heatmap_data[js_timestamp // 1000] = word_count
            
        except (ValueError, IndexError) as e:
            print(f"Error processing date {row['date']}: {e}")
            continue
    
    return heatmap_data

def generate_html():
    """
    Generate HTML/JavaScript code for the heatmap visualization
    """
    heatmap_data = create_heatmap_data()
    if not heatmap_data:
        return None
    
    # Convert data to JSON string
    data_json = json.dumps(heatmap_data)
    
    # Calculate min and max to set the color scale
    values = list(heatmap_data.values())
    min_value = min(values) if values else 0
    max_value = max(values) if values else 1000
    
    # Get the earliest and latest dates to set the range
    if values:
        dates = [datetime.fromtimestamp(int(ts)) for ts in heatmap_data.keys()]
        min_date = min(dates)
        max_date = max(dates)
    else:
        # Default to a range if no data
        min_date = datetime(1568, 1, 1)
        max_date = datetime(1571, 12, 31)
    
    # Calculate range to include full years
    start_year = min_date.year
    end_year = max_date.year
    
    # Create an HTML component for Docusaurus
    html = f"""
import React, {{ useEffect, useRef }} from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

// Component that loads CalHeatmap only in browser context
const CavrianaHeatmap = () => {{
  return (
    <BrowserOnly>
      {{() => {{
        try {{
          // Dynamic import will happen in the nested component
          return <HeatmapContent />;
        }} catch (error) {{
          console.error("Error loading calendar heatmap:", error);
          return <div>Error loading correspondence heatmap. Please check console for details.</div>;
        }}
      }}}}
    </BrowserOnly>
  );
}};

// The actual heatmap content
const HeatmapContent = () => {{
  const calendarEl = useRef(null);
  const tooltipEl = useRef(null);
  const legendEl = useRef(null);

  useEffect(() => {{
    // Import dynamically since we're in the browser
    const loadLibraries = async () => {{
      try {{
        // Import required libraries
        const CalHeatmapModule = await import('cal-heatmap');
        const CalHeatmap = CalHeatmapModule.default;
        await import('cal-heatmap/cal-heatmap.css');
        
        // Create a new instance
        const cal = new CalHeatmap();
        
        // Initialize with data
        const data = {data_json};

        // Create legend
        const legend = document.createElement('div');
        legend.className = 'ch-legend';
        if (legendEl.current) {{
          legendEl.current.appendChild(legend);
        }}

        // Initialize the calendar
        cal.init({{
          itemSelector: calendarEl.current,
          legendElement: legend,
          domain: {{
            type: 'year',
            gutter: 10,
            label: {{ text: 'Year', textAlign: 'start', position: 'top' }},
          }},
          subDomain: {{ 
            type: 'day',
            label: 'D',
            width: 11,
            height: 11,
            gutter: 2,
            radius: 2,
          }},
          date: {{ start: new Date({start_year}, 0, 1) }},
          range: {end_year - start_year + 1},
          data: {{
            source: data,
            type: 'json',
            x: d => +d,
            y: d => +data[d],
          }},
          scale: {{
            color: {{
              type: 'linear',
              domain: [{min_value}, {max_value}],
              scheme: 'YlGnBu'
            }}
          }},
          tooltip: {{
            enabled: true,
            text: function(date, value) {{
              if (!value) return 'No letters on this day';
              const dateObj = new Date(date * 1000);
              const formattedDate = dateObj.toLocaleDateString('en-US', {{ 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              }});
              return `<strong>${{formattedDate}}</strong>: ${{value}} words`;
            }}
          }}
        }});

        return () => {{
          cal.destroy();
        }};
      }} catch (error) {{
        console.error('Failed to load CalHeatmap:', error);
        if (calendarEl.current) {{
          calendarEl.current.innerHTML = '<p>Failed to load calendar visualization</p>';
        }}
      }}
    }};

    loadLibraries();
  }}, []);

  return (
    <div className="cavriana-heatmap">
      <h2>Cavriana's Letter-Writing Activity</h2>
      <p>The heatmap below shows the volume of Filippo Cavriana's correspondence (in word count) over time. Each colored cell represents a day when Cavriana wrote a letter, with darker colors indicating more words written.</p>
      <div ref={{calendarEl}} className="cal-heatmap"></div>
      <div ref={{legendEl}} className="cal-heatmap-legend"></div>
      <div ref={{tooltipEl}} className="cal-heatmap-tooltip"></div>
      <div className="cal-heatmap-info">
        <p>Hover over a colored cell to see the exact number of words written on that day.</p>
        <p className="cal-heatmap-updated">Last updated: {datetime.now().strftime('%Y-%m-%d')}</p>
      </div>
    </div>
  );
}};

export default CavrianaHeatmap;
"""
    
    return html

def save_heatmap_component():
    """
    Generate and save the heatmap React component for Docusaurus
    """
    html_content = generate_html()
    if html_content:
        # Save as a React component
        with open('CavrianaHeatmap.jsx', 'w') as f:
            f.write(html_content)
        print(f"Heatmap component saved as CavrianaHeatmap.jsx")
        
        # Also output a message about required dependencies
        print("\nTo use this component in your Docusaurus site, you need to install these dependencies:")
        print("npm install cal-heatmap d3 @docusaurus/BrowserOnly")
        print("\nAdd the component to your intro.md file with:")
        print("import CavrianaHeatmap from '@site/src/components/CavrianaHeatmap';")
        print("\n<CavrianaHeatmap />")
        
        return True
    return False

def main():
    """Main function to generate the heatmap"""
    # Check if letter_metadata.csv exists, if not, run letter_parser.py
    if not os.path.exists('letter_metadata.csv'):
        print("Letter metadata not found. Running letter_parser.py to generate it...")
        import letter_parser
        letter_parser.main()
    
    print("Generating Calendar Heatmap for Cavriana's correspondence...")
    success = save_heatmap_component()
    
    if success:
        print("Heatmap generation completed successfully!")
    else:
        print("Failed to generate heatmap. Please check the error messages above.")

if __name__ == "__main__":
    main()