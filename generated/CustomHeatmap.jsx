/* templates/CustomHeatmap.template.jsx
   ---------------------------------------------------------------
   React component produced by scripts/generate_heatmap.py.
   Renders a single-year GitHub-style heat-map with arrow navigation.
*/

import React, { useState, useRef, useEffect } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import useBaseUrl from '@docusaurus/useBaseUrl';

/* overwritten by generate_heatmap.py */
const YEARS = [1568, 1569, 1570, 1571, 1572, 1574];
const rows  = [
  {
    "date": "1568-04-06",
    "value": 544,
    "slugs": [
      "1568-04-06"
    ]
  },
  {
    "date": "1568-04-28",
    "value": 786,
    "slugs": [
      "1568-04-28"
    ]
  },
  {
    "date": "1568-05-04",
    "value": 780,
    "slugs": [
      "1568-05-04"
    ]
  },
  {
    "date": "1568-05-05",
    "value": 494,
    "slugs": [
      "1568-05-05"
    ]
  },
  {
    "date": "1568-05-28",
    "value": 488,
    "slugs": [
      "1568-05-28"
    ]
  },
  {
    "date": "1568-06-09",
    "value": 410,
    "slugs": [
      "1568-06-09"
    ]
  },
  {
    "date": "1568-07-03",
    "value": 492,
    "slugs": [
      "1568-07-03"
    ]
  },
  {
    "date": "1568-07-24",
    "value": 538,
    "slugs": [
      "1568-07-24"
    ]
  },
  {
    "date": "1568-09-07",
    "value": 854,
    "slugs": [
      "1568-09-07"
    ]
  },
  {
    "date": "1569-01-03",
    "value": 1242,
    "slugs": [
      "1569-01-03"
    ]
  },
  {
    "date": "1569-11-29",
    "value": 500,
    "slugs": [
      "1569-11-29"
    ]
  },
  {
    "date": "1569-12-21",
    "value": 646,
    "slugs": [
      "1569-12-21"
    ]
  },
  {
    "date": "1570-03-20",
    "value": 756,
    "slugs": [
      "1570-03-20"
    ]
  },
  {
    "date": "1570-05-20",
    "value": 1880,
    "slugs": [
      "1570-05-20"
    ]
  },
  {
    "date": "1570-07-15",
    "value": 2314,
    "slugs": [
      "1570-07-15"
    ]
  },
  {
    "date": "1570-07-29",
    "value": 2354,
    "slugs": [
      "1570-07-29",
      "1570-07-29-b"
    ]
  },
  {
    "date": "1570-08-08",
    "value": 704,
    "slugs": [
      "1570-08-08-c"
    ]
  },
  {
    "date": "1570-08-17",
    "value": 3324,
    "slugs": [
      "1570-08-17"
    ]
  },
  {
    "date": "1570-09-01",
    "value": 5432,
    "slugs": [
      "1570-09-01"
    ]
  },
  {
    "date": "1570-09-11",
    "value": 3826,
    "slugs": [
      "1570-09-11"
    ]
  },
  {
    "date": "1570-09-14",
    "value": 436,
    "slugs": [
      "1570-09-14"
    ]
  },
  {
    "date": "1570-10-03",
    "value": 912,
    "slugs": [
      "1570-10-03"
    ]
  },
  {
    "date": "1570-10-13",
    "value": 4499,
    "slugs": [
      "1570-10-13"
    ]
  },
  {
    "date": "1570-11-02",
    "value": 1757,
    "slugs": [
      "1570-11-02",
      "1570-11-02-b"
    ]
  },
  {
    "date": "1570-11-04",
    "value": 1976,
    "slugs": [
      "1570-11-04"
    ]
  },
  {
    "date": "1570-11-09",
    "value": 278,
    "slugs": [
      "1570-11-09"
    ]
  },
  {
    "date": "1571-01-12",
    "value": 4434,
    "slugs": [
      "1571-01-12"
    ]
  },
  {
    "date": "1571-01-14",
    "value": 3688,
    "slugs": [
      "1571-01-14"
    ]
  },
  {
    "date": "1571-01-26",
    "value": 2460,
    "slugs": [
      "1571-01-26"
    ]
  },
  {
    "date": "1571-02-06",
    "value": 2081,
    "slugs": [
      "1571-02-06"
    ]
  },
  {
    "date": "1571-03-31",
    "value": 2170,
    "slugs": [
      "1571-03-31"
    ]
  },
  {
    "date": "1571-04-18",
    "value": 328,
    "slugs": [
      "1571-04-18"
    ]
  },
  {
    "date": "1571-04-19",
    "value": 1396,
    "slugs": [
      "1571-04-19"
    ]
  },
  {
    "date": "1571-06-27",
    "value": 630,
    "slugs": [
      "1571-06-27"
    ]
  },
  {
    "date": "1571-07-07",
    "value": 1296,
    "slugs": [
      "1571-07-07"
    ]
  },
  {
    "date": "1571-07-15",
    "value": 328,
    "slugs": [
      "1571-07-15"
    ]
  },
  {
    "date": "1571-08-14",
    "value": 572,
    "slugs": [
      "1571-08-14"
    ]
  },
  {
    "date": "1572-02-06",
    "value": 959,
    "slugs": [
      "1572-02-06"
    ]
  },
  {
    "date": "1572-02-12",
    "value": 878,
    "slugs": [
      "1572-02-12"
    ]
  },
  {
    "date": "1572-03-08",
    "value": 1880,
    "slugs": [
      "1572-03-08"
    ]
  },
  {
    "date": "1572-03-19",
    "value": 1526,
    "slugs": [
      "1572-03-19"
    ]
  },
  {
    "date": "1572-04-22",
    "value": 2540,
    "slugs": [
      "1572-04-22"
    ]
  },
  {
    "date": "1572-05-12",
    "value": 4294,
    "slugs": [
      "1572-05-12"
    ]
  },
  {
    "date": "1572-05-28",
    "value": 3088,
    "slugs": [
      "1572-05-28"
    ]
  },
  {
    "date": "1572-07-12",
    "value": 1460,
    "slugs": [
      "1572-07-12"
    ]
  },
  {
    "date": "1572-07-19",
    "value": 1406,
    "slugs": [
      "1572-07-19"
    ]
  },
  {
    "date": "1572-08-04",
    "value": 4764,
    "slugs": [
      "1572-08-04"
    ]
  },
  {
    "date": "1572-08-31",
    "value": 1290,
    "slugs": [
      "1572-08-31"
    ]
  },
  {
    "date": "1572-10-23",
    "value": 868,
    "slugs": [
      "1572-10-23"
    ]
  },
  {
    "date": "1572-11-04",
    "value": 1224,
    "slugs": [
      "1572-11-04"
    ]
  },
  {
    "date": "1572-11-20",
    "value": 204,
    "slugs": [
      "1572-11-20"
    ]
  },
  {
    "date": "1572-11-21",
    "value": 4121,
    "slugs": [
      "1572-11-21"
    ]
  },
  {
    "date": "1572-11-27",
    "value": 1322,
    "slugs": [
      "1572-11-27"
    ]
  },
  {
    "date": "1572-12-01",
    "value": 2254,
    "slugs": [
      "1572-12-01"
    ]
  },
  {
    "date": "1572-12-07",
    "value": 1832,
    "slugs": [
      "1572-12-07"
    ]
  },
  {
    "date": "1574-03-06",
    "value": 1927,
    "slugs": [
      "1574-03-06"
    ]
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

// How much was written in each year, on the same measure the day cells use,
// so a reader can see at a glance which years the correspondence is thickest in.
const YEAR_TOTALS = YEARS.map((y) =>
  rows.filter((r) => r.date.startsWith(String(y))).reduce((s, r) => s + r.value, 0),
);
const YEAR_LETTERS = YEARS.map((y) =>
  rows.filter((r) => r.date.startsWith(String(y)))
      .reduce((s, r) => s + ((r.slugs && r.slugs.length) || 0), 0),
);
const MAX_LETTERS = Math.max(...YEAR_LETTERS, 0);

// The day cells step through five fixed shades, which is right for a single
// day but too coarse for six years: it put 1 letter and 9 in the same bucket,
// and 15 and 18 in another. The years therefore blend continuously through the
// same five colours, so each reads as its own weight.
// Pick whichever of ink or paper reads better on the shade, rather than
// guessing a cut-off: at the middle of the ramp dark text wins, and a fixed
// threshold put white on a green where it fell below legibility.
const luminance = (rgb) => {
  const lin = (v) => {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * lin(rgb[0]) + 0.7152 * lin(rgb[1]) + 0.0722 * lin(rgb[2]);
};

// Compare the ink colours actually used, not idealised black and white: the
// middle greens are dark enough to defeat white and light enough to defeat a
// soft near-black, and only true black clears the threshold on them.
const readableOn = (rgb) => {
  const L = luminance(rgb);
  const contrast = (other) => {
    const M = luminance(other);
    return (Math.max(L, M) + 0.05) / (Math.min(L, M) + 0.05);
  };
  return contrast([255, 255, 255]) > contrast([0, 0, 0]) ? '#ffffff' : '#000000';
};

const yearRGB = (n) => {
  if (!n) return [235, 237, 240];
  const ramp = ['#9be9a8', '#40c463', '#30a14e', '#216e39', '#0a4620'];
  const p = (n / (MAX_LETTERS || 1)) * (ramp.length - 1);
  const i = Math.min(Math.floor(p), ramp.length - 2);
  const f = p - i;
  const hex = (c) => [1, 3, 5].map((k) => parseInt(c.slice(k, k + 2), 16));
  const a = hex(ramp[i]);
  const b = hex(ramp[i + 1]);
  return a.map((v, k) => Math.round(v + (b[k] - v) * f));
};

const yearShade = (n) => {
  return `rgb(${yearRGB(n).join(',')})`;
};

const HeatmapDisplay = () => {
  const [yearIx, setYearIx] = useState(0);
  const [tooltipContent, setTooltipContent] = useState('');
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });
  const [showTooltip, setShowTooltip] = useState(false);
  const svgRef = useRef(null);
  const [selectedDay, setSelectedDay] = useState(null);
  const docsBase = useBaseUrl('/docs/');
  
  // Current year and data for that year
  const currentYear = YEARS[yearIx];
  
  // Filter data for current year
  const yearData = rows.filter(row => row.date.startsWith(String(currentYear)));
  
  // Values are already summed per day by the generator, which also supplies
  // every letter written that day so a cell can link to them.
  const valueMap = {};
  const slugMap = {};
  yearData.forEach(item => {
    valueMap[item.date] = item.value;
    slugMap[item.date] = item.slugs || [];
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
  const showCellTooltip = (date, value, e, letterCount = 0) => {
    const rect = e.target.getBoundingClientRect();

    // Format date for display. Build the Date from components: parsing the
    // 'YYYY-MM-DD' string yields UTC midnight, which formats as the previous
    // day for viewers in negative-offset zones.
    const [dy, dm, dd] = date.split('-').map(Number);
    const displayDate = new Date(dy, dm - 1, dd);
    const formattedDate = displayDate.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });

    // Set tooltip content and position (fixed to viewport)
    setTooltipContent(
      letterCount
        ? `${formattedDate}: ${letterCount === 1 ? '1 letter' : `${letterCount} letters`}, ${value} words`
        : `No letters on ${formattedDate}`
    );

    setTooltipPosition({
      x: rect.left + rect.width / 2,
      y: rect.top
    });

    setShowTooltip(true);
  };
  
  const hideTooltip = () => {
    setShowTooltip(false);
  };

  const letterHref = (slug) => `${docsBase}${slug.slice(0, 4)}/${slug}`;

  const openDay = (day) => {
    if (!day.slugs.length) {
      return;
    }
    if (day.slugs.length === 1) {
      window.location.assign(letterHref(day.slugs[0]));
      return;
    }
    setSelectedDay(day);
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
    
    // Group days into calendar weeks (columns = weeks, rows = weekdays)
    const jan1DayOfWeek = new Date(currentYear, 0, 1).getDay(); // 0=Sun … 6=Sat
    daysInYear.forEach((date) => {
      const dayOfWeek = date.getDay(); // 0-6 (Sunday to Saturday)
      // Day-of-year (0-based)
      const dayOfYear = Math.floor((date - new Date(currentYear, 0, 1)) / 86400000);
      // Week column: offset by Jan 1's weekday so each column is a real calendar week
      const weekOfYear = Math.floor((dayOfYear + jan1DayOfWeek) / 7);

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
        slugs: slugMap[dateStr] || [],
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
                className={day.slugs.length ? 'day-cell day-cell--has-letters' : 'day-cell'}
                data-date={day.date}
                data-value={day.value}
                onMouseEnter={(e) => showCellTooltip(day.date, day.value, e, day.slugs.length)}
                onMouseLeave={hideTooltip}
                onClick={() => openDay(day)}
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
        {YEARS.map((year, i) => {
          const shade = yearShade(YEAR_LETTERS[i]);
          const ink = readableOn(yearRGB(YEAR_LETTERS[i]));
          return (
            <button
              key={year}
              onClick={() => jumpTo(i)}
              className={yearIx === i ? 'active' : ''}
              style={{backgroundColor: shade, color: ink}}
              title={`${year}: ${YEAR_LETTERS[i]} ${
                YEAR_LETTERS[i] === 1 ? 'letter' : 'letters'
              }, ${YEAR_TOTALS[i].toLocaleString()} words`}
            >
              {year}
            </button>
          );
        })}
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
                position: 'fixed',
                left: `${tooltipPosition.x}px`,
                top: `${tooltipPosition.y - 8}px`,
                transform: 'translate(-50%, -100%)',
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                color: 'white',
                padding: '5px 10px',
                borderRadius: '4px',
                fontSize: '14px',
                pointerEvents: 'none',
                zIndex: 9999
              }}
            >
              {tooltipContent}
            </div>
          )}
        </div>
      </div>
      
      {/* Color legend */}
      {/* A day carrying several letters lists them here rather than in the
          tooltip, so the links stay put and can actually be clicked. */}
      {selectedDay && (
        <div className="heatmap-day-letters">
          <span className="heatmap-day-letters__label">
            {selectedDay.slugs.length} letters on {selectedDay.date}
          </span>
          {selectedDay.slugs.map((slug) => (
            <a key={slug} href={letterHref(slug)} className="heatmap-day-letters__link">
              {slug}
            </a>
          ))}
          <button
            type="button"
            className="heatmap-day-letters__close"
            onClick={() => setSelectedDay(null)}
            aria-label="Dismiss">
            ×
          </button>
        </div>
      )}

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