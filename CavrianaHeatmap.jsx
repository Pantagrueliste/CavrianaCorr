
import React, { useEffect, useRef } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

// Component that loads CalHeatmap only in browser context
const CavrianaHeatmap = () => {
  return (
    <BrowserOnly>
      {() => {
        try {
          // Dynamic import will happen in the nested component
          return <HeatmapContent />;
        } catch (error) {
          console.error("Error loading calendar heatmap:", error);
          return <div>Error loading correspondence heatmap. Please check console for details.</div>;
        }
      }}
    </BrowserOnly>
  );
};

// The actual heatmap content
const HeatmapContent = () => {
  const calendarEl = useRef(null);
  const tooltipEl = useRef(null);
  const legendEl = useRef(null);

  useEffect(() => {
    // Import dynamically since we're in the browser
    const loadLibraries = async () => {
      try {
        // Import required libraries
        const CalHeatmapModule = await import('cal-heatmap');
        const CalHeatmap = CalHeatmapModule.default;
        await import('cal-heatmap/cal-heatmap.css');
        
        // Create a new instance
        const cal = new CalHeatmap();
        
        // Initialize with data
        const data = {"-12677644725": 544, "-12675743925": 786, "-12675225525": 780, "-12675139125": 494, "-12673151925": 488, "-12672115125": 406, "-12670041525": 490, "-12668227125": 538, "-12664339125": 854, "-12654143925": 1238, "-12625631925": 500, "-12623731125": 648, "-12610771125": 1876, "-12605932725": 2314, "-12604723125": 1738, "-12603081525": 3314, "-12601785525": 5380, "-12600921525": 3826, "-12600662325": 436, "-12599020725": 912, "-12596428725": 864, "-12595823925": 278, "-12590121525": 3903, "-12581999925": 328, "-12574396725": 326};

        // Create legend
        const legend = document.createElement('div');
        legend.className = 'ch-legend';
        if (legendEl.current) {
          legendEl.current.appendChild(legend);
        }

        // Initialize the calendar
        cal.init({
          itemSelector: calendarEl.current,
          legendElement: legend,
          domain: {
            type: 'year',
            gutter: 10,
            label: { text: 'Year', textAlign: 'start', position: 'top' },
          },
          subDomain: { 
            type: 'day',
            label: 'D',
            width: 11,
            height: 11,
            gutter: 2,
            radius: 2,
          },
          date: { start: new Date(1568, 0, 1) },
          range: 4,
          data: {
            source: data,
            type: 'json',
            x: d => +d,
            y: d => +data[d],
          },
          scale: {
            color: {
              type: 'linear',
              domain: [278, 5380],
              scheme: 'YlGnBu'
            }
          },
          tooltip: {
            enabled: true,
            text: function(date, value) {
              if (!value) return 'No letters on this day';
              const dateObj = new Date(date * 1000);
              const formattedDate = dateObj.toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              });
              return `<strong>${formattedDate}</strong>: ${value} words`;
            }
          }
        });

        return () => {
          cal.destroy();
        };
      } catch (error) {
        console.error('Failed to load CalHeatmap:', error);
        if (calendarEl.current) {
          calendarEl.current.innerHTML = '<p>Failed to load calendar visualization</p>';
        }
      }
    };

    loadLibraries();
  }, []);

  return (
    <div className="cavriana-heatmap">
      <h2>Cavriana's Letter-Writing Activity</h2>
      <p>The heatmap below shows the volume of Filippo Cavriana's correspondence (in word count) over time. Each colored cell represents a day when Cavriana wrote a letter, with darker colors indicating more words written.</p>
      <div ref={calendarEl} className="cal-heatmap"></div>
      <div ref={legendEl} className="cal-heatmap-legend"></div>
      <div ref={tooltipEl} className="cal-heatmap-tooltip"></div>
      <div className="cal-heatmap-info">
        <p>Hover over a colored cell to see the exact number of words written on that day.</p>
        <p className="cal-heatmap-updated">Last updated: 2025-04-25</p>
      </div>
    </div>
  );
};

export default CavrianaHeatmap;
