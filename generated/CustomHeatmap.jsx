/* templates/CustomHeatmap.template.jsx
   ---------------------------------------------------------------
   React component produced by scripts/generate_heatmap.py.
   Renders a single-year GitHub-style heat-map with arrow navigation.
*/

import React, { useState, useRef, useEffect } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

/* overwritten by generate_heatmap.py */
const YEARS = [1568, 1569, 1570, 1571];
const rows  = [
  {
    "date": "1568-04-06",
    "value": 544
  },
  {
    "date": "1568-04-28",
    "value": 786
  },
  {
    "date": "1568-05-04",
    "value": 780
  },
  {
    "date": "1568-05-05",
    "value": 494
  },
  {
    "date": "1568-05-28",
    "value": 488
  },
  {
    "date": "1568-06-09",
    "value": 410
  },
  {
    "date": "1568-07-03",
    "value": 490
  },
  {
    "date": "1568-07-24",
    "value": 538
  },
  {
    "date": "1568-09-07",
    "value": 854
  },
  {
    "date": "1569-01-03",
    "value": 1238
  },
  {
    "date": "1569-11-29",
    "value": 500
  },
  {
    "date": "1569-12-21",
    "value": 648
  },
  {
    "date": "1570-05-20",
    "value": 1876
  },
  {
    "date": "1570-07-15",
    "value": 2314
  },
  {
    "date": "1570-07-29",
    "value": 1738
  },
  {
    "date": "1570-08-17",
    "value": 3314
  },
  {
    "date": "1570-09-01",
    "value": 5380
  },
  {
    "date": "1570-09-11",
    "value": 3826
  },
  {
    "date": "1570-09-14",
    "value": 436
  },
  {
    "date": "1570-10-03",
    "value": 912
  },
  {
    "date": "1570-10-11",
    "value": 3348
  },
  {
    "date": "1570-11-02",
    "value": 894
  },
  {
    "date": "1570-11-04",
    "value": 1972
  },
  {
    "date": "1570-11-09",
    "value": 278
  },
  {
    "date": "1571-01-14",
    "value": 3903
  },
  {
    "date": "1571-04-18",
    "value": 328
  },
  {
    "date": "1571-04-19",
    "value": 1394
  },
  {
    "date": "1571-07-15",
    "value": 326
  }
];   // [{date:'YYYY-MM-DD', value}, …]

const CavrianaHeatmap = () => (
  <BrowserOnly fallback={<div>Loading heat-map…</div>}>
    {() => <HeatmapDisplay />}
  </BrowserOnly>
);

// Helper to get an array of all days in a year
const getDaysInYear = (year) => {
  const daysArray = [];
  const startDate = new Date(year, 0, 1); // January 1st of the year
  const endDate = new Date(year, 11, 31); // December 31st of the year
  
  // Fill array with all dates from start to end
  let currentDate = new Date(startDate);
  while (currentDate <= endDate) {
    daysArray.push(new Date(currentDate));
    currentDate.setDate(currentDate.getDate() + 1);
  }
  
  return daysArray;
};

// Format date as YYYY-MM-DD
const formatDateString = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

// Get month name abbreviation
const getMonthAbbr = (monthIndex) => {
  return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][monthIndex];
};

// Quantized color scale for the heatmap
const getColorForValue = (value, maxValue) => {
  if (!value) return '#ebedf0'; // No activity - light gray
  
  // Define 5 color steps from light to dark
  const colors = [
    '#9be9a8', // Light green
    '#40c463', // Medium green
    '#30a14e', // Medium-dark green
    '#216e39', // Dark green
    '#0a4620'  // Very dark green
  ];
  
  if (maxValue === 0) return colors[0];
  
  // Calculate which color to use based on percentage of max value
  const percentage = value / maxValue;
  const colorIndex = Math.min(Math.floor(percentage * colors.length), colors.length - 1);
  return colors[colorIndex];
};

const HeatmapDisplay = () => {
  const [yearIx, setYearIx] = useState(0);
  const [tooltipContent, setTooltipContent] = useState('');
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });
  const [showTooltip, setShowTooltip] = useState(false);
  const svgRef = useRef(null);
  
  // Current year and data for that year
  const currentYear = YEARS[yearIx];
  
  // Filter data for current year
  const yearData = rows.filter(row => row.date.startsWith(String(currentYear)));
  
  // Create a map for quick lookup of values by date string
  const valueMap = {};
  yearData.forEach(item => {
    valueMap[item.date] = item.value;
  });
  
  // Get max value for color scaling
  const maxValue = yearData.length 
    ? Math.max(...yearData.map(item => item.value))
    : 0;
  
  // Navigation functions
  const prev = () => yearIx > 0 && setYearIx(yearIx - 1);
  const next = () => yearIx < YEARS.length - 1 && setYearIx(yearIx + 1);
  const jumpTo = (i) => setYearIx(i);

  // Handle tooltip display
  const showCellTooltip = (date, value, e) => {
    const rect = e.target.getBoundingClientRect();
    const svgRect = svgRef.current.getBoundingClientRect();
    
    // Format date for display
    const displayDate = new Date(date);
    const formattedDate = displayDate.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
    
    // Set tooltip content and position
    setTooltipContent(
      value 
        ? `${formattedDate}: ${value} words`
        : `No letters on ${formattedDate}`
    );
    
    setTooltipPosition({
      x: rect.left - svgRect.left + rect.width / 2,
      y: rect.top - svgRect.top
    });
    
    setShowTooltip(true);
  };
  
  const hideTooltip = () => {
    setShowTooltip(false);
  };
  
  // Generate the heatmap grid
  const renderHeatmap = () => {
    const cellSize = 12;
    const cellGap = 3;
    const weekCount = 53; // Max number of weeks in a year (52 weeks + potential partial week)
    const dayCount = 7; // Days in a week
    const monthLabelHeight = 20;
    
    // Width and height calculations
    const svgWidth = weekCount * (cellSize + cellGap);
    const svgHeight = dayCount * (cellSize + cellGap) + monthLabelHeight;
    
    // Get all days in the year for the grid
    const daysInYear = getDaysInYear(currentYear);
    
    // Track month transitions to display month labels
    let lastMonth = -1;
    const monthLabels = [];
    const weeks = [];
    
    // Group days into weeks for rendering
    daysInYear.forEach((date, index) => {
      const dayOfWeek = date.getDay(); // 0-6 (Sunday to Saturday)
      const weekOfYear = Math.floor(index / 7);
      
      // Add month labels when month changes
      if (date.getMonth() !== lastMonth) {
        lastMonth = date.getMonth();
        const monthName = getMonthAbbr(lastMonth);
        monthLabels.push({
          month: monthName,
          x: weekOfYear * (cellSize + cellGap)
        });
      }
      
      // Create week array if it doesn't exist
      if (!weeks[weekOfYear]) {
        weeks[weekOfYear] = [];
      }
      
      // Add day to the week
      const dateStr = formatDateString(date);
      const value = valueMap[dateStr] || 0;
      
      weeks[weekOfYear][dayOfWeek] = {
        date: dateStr,
        value: value,
        day: dayOfWeek,
        week: weekOfYear
      };
    });
    
    return (
      <svg 
        ref={svgRef}
        width={svgWidth} 
        height={svgHeight} 
        className="cavriana-heatmap-grid"
      >
        {/* Month labels at the top */}
        {monthLabels.map((label, idx) => (
          <text 
            key={`month-${idx}`}
            x={label.x}
            y={14}
            className="month-label"
            fontSize={10}
          >
            {label.month}
          </text>
        ))}
        
        {/* Render day cells by weeks and days */}
        {weeks.map((week, weekIdx) => (
          // Week column
          <g key={`week-${weekIdx}`}>
            {week.map((day, dayIdx) => day && (
              // Day cell 
              <rect
                key={`day-${day.date}`}
                x={day.week * (cellSize + cellGap)}
                y={(day.day * (cellSize + cellGap)) + monthLabelHeight}
                width={cellSize}
                height={cellSize}
                rx={2}
                ry={2}
                fill={getColorForValue(day.value, maxValue)}
                className="day-cell"
                data-date={day.date}
                data-value={day.value}
                onMouseEnter={(e) => showCellTooltip(day.date, day.value, e)}
                onMouseLeave={hideTooltip}
              />
            ))}
          </g>
        ))}
      </svg>
    );
  };
  
  // Render the legend with color scale
  const renderLegend = () => {
    const legendItems = [
      { label: 'Less', color: '#ebedf0' },
      { color: '#9be9a8' },
      { color: '#40c463' },
      { color: '#30a14e' },
      { color: '#216e39' },
      { label: 'More', color: '#0a4620' }
    ];
    
    return (
      <div className="cavriana-heatmap-legend">
        <span>Less</span>
        {legendItems.map((item, idx) => (
          <span 
            key={`legend-${idx}`} 
            className="legend-item"
            style={{
              backgroundColor: item.color,
              width: '12px',
              height: '12px',
              margin: '0 2px',
              display: 'inline-block',
              borderRadius: '2px'
            }}
          />
        ))}
        <span>More</span>
      </div>
    );
  };
  
  // Re-render the heatmap when the year changes
  useEffect(() => {
    // Reset tooltip when year changes
    setShowTooltip(false);
    
    // This key change will ensure the SVG re-renders completely
  }, [yearIx, currentYear]);
  
  return (
    <div className="cavriana-heatmap-custom">
      <h2>Cavriana Letter-Writing Activity – {currentYear}</h2>
      
      {/* Year selection buttons */}
      <div className="year-selector">
        {YEARS.map((year, i) => (
          <button 
            key={year} 
            onClick={() => jumpTo(i)}
            className={yearIx === i ? 'active' : ''}
          >
            {year}
          </button>
        ))}
      </div>
      
      {/* Main heatmap grid */}
      <div className="heatmap-container">
        {/* Using a key based on the year ensures complete remounting */}
        <div key={`heatmap-${currentYear}`} className="heatmap-grid">
          {renderHeatmap()}
          
          {/* Tooltip */}
          {showTooltip && (
            <div 
              className="heatmap-tooltip"
              style={{
                position: 'absolute',
                left: `${tooltipPosition.x}px`,
                top: `${tooltipPosition.y - 40}px`,
                transform: 'translateX(-50%)',
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                color: 'white',
                padding: '5px 10px',
                borderRadius: '4px',
                fontSize: '14px',
                pointerEvents: 'none',
                zIndex: 10
              }}
            >
              {tooltipContent}
            </div>
          )}
        </div>
      </div>
      
      {/* Color legend */}
      {renderLegend()}
      
      {/* Year navigation buttons */}
      <div className="year-navigation">
        <button onClick={prev} disabled={yearIx === 0}>◀︎</button>
        <span>{currentYear}</span>
        <button onClick={next} disabled={yearIx === YEARS.length - 1}>▶︎</button>
      </div>
    </div>
  );
};

export default CavrianaHeatmap;