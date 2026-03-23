/* templates/CavrianaHeatmap.template.jsx
   ---------------------------------------------------------------
   React component produced by scripts/generate_heatmap.py.
   Renders a single-year GitHub-style heat-map with arrow navigation.
*/

import React, { useEffect, useState, useRef } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

import CalHeatmap  from 'cal-heatmap';
import LegendLite  from 'cal-heatmap/plugins/LegendLite';
import Tooltip     from 'cal-heatmap/plugins/Tooltip';
import 'cal-heatmap/cal-heatmap.css';

// import * as d3 from 'd3'; // CalHeatmap v4+ bundles its own D3, this might not be needed or could conflict. Try commenting out if issues persist.

/* overwritten by generate_heatmap.py */
const YEARS = [1566, 1568, 1569, 1570, 1571, 1572, 1574];
const rows  = [
  {
    "date": "1566-12-31",
    "value": 0
  },
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
    "value": 492
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
    "date": "1569-03-11",
    "value": 0
  },
  {
    "date": "1569-11-29",
    "value": 500
  },
  {
    "date": "1569-12-09",
    "value": 0
  },
  {
    "date": "1569-12-21",
    "value": 648
  },
  {
    "date": "1569-12-31",
    "value": 0
  },
  {
    "date": "1570-03-20",
    "value": 756
  },
  {
    "date": "1570-03-30",
    "value": 0
  },
  {
    "date": "1570-05-20",
    "value": 1876
  },
  {
    "date": "1570-05-30",
    "value": 0
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
    "date": "1570-08-08",
    "value": 0
  },
  {
    "date": "1570-08-17",
    "value": 3316
  },
  {
    "date": "1570-08-27",
    "value": 0
  },
  {
    "date": "1570-09-01",
    "value": 5416
  },
  {
    "date": "1570-09-09",
    "value": 0
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
    "date": "1570-09-24",
    "value": 0
  },
  {
    "date": "1570-10-03",
    "value": 912
  },
  {
    "date": "1570-10-09",
    "value": 0
  },
  {
    "date": "1570-10-13",
    "value": 4497
  },
  {
    "date": "1570-10-23",
    "value": 0
  },
  {
    "date": "1570-11-02",
    "value": 898
  },
  {
    "date": "1570-11-04",
    "value": 1974
  },
  {
    "date": "1570-11-07",
    "value": 0
  },
  {
    "date": "1570-11-09",
    "value": 278
  },
  {
    "date": "1570-11-12",
    "value": 0
  },
  {
    "date": "1571-01-12",
    "value": 4424
  },
  {
    "date": "1571-01-14",
    "value": 3688
  },
  {
    "date": "1571-01-26",
    "value": 2458
  },
  {
    "date": "1571-02-05",
    "value": 0
  },
  {
    "date": "1571-02-06",
    "value": 2081
  },
  {
    "date": "1571-03-31",
    "value": 2170
  },
  {
    "date": "1571-04-10",
    "value": 0
  },
  {
    "date": "1571-04-11",
    "value": 0
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
    "date": "1571-04-28",
    "value": 0
  },
  {
    "date": "1571-06-02",
    "value": 0
  },
  {
    "date": "1571-06-27",
    "value": 628
  },
  {
    "date": "1571-07-07",
    "value": 1296
  },
  {
    "date": "1571-07-10",
    "value": 0
  },
  {
    "date": "1571-07-15",
    "value": 328
  },
  {
    "date": "1571-07-17",
    "value": 0
  },
  {
    "date": "1571-08-08",
    "value": 0
  },
  {
    "date": "1571-08-14",
    "value": 572
  },
  {
    "date": "1571-08-24",
    "value": 0
  },
  {
    "date": "1571-09-28",
    "value": 0
  },
  {
    "date": "1571-11-04",
    "value": 0
  },
  {
    "date": "1571-12-08",
    "value": 0
  },
  {
    "date": "1571-12-11",
    "value": 0
  },
  {
    "date": "1572-01-22",
    "value": 0
  },
  {
    "date": "1572-02-06",
    "value": 959
  },
  {
    "date": "1572-02-12",
    "value": 878
  },
  {
    "date": "1572-03-08",
    "value": 1870
  },
  {
    "date": "1572-03-19",
    "value": 1520
  },
  {
    "date": "1572-03-29",
    "value": 0
  },
  {
    "date": "1572-04-17",
    "value": 0
  },
  {
    "date": "1572-04-22",
    "value": 2538
  },
  {
    "date": "1572-05-02",
    "value": 0
  },
  {
    "date": "1572-05-28",
    "value": 3076
  },
  {
    "date": "1572-06-07",
    "value": 0
  },
  {
    "date": "1572-06-12",
    "value": 0
  },
  {
    "date": "1572-06-13",
    "value": 0
  },
  {
    "date": "1572-07-12",
    "value": 1458
  },
  {
    "date": "1572-07-19",
    "value": 1402
  },
  {
    "date": "1572-07-22",
    "value": 0
  },
  {
    "date": "1572-07-29",
    "value": 0
  },
  {
    "date": "1572-08-04",
    "value": 4754
  },
  {
    "date": "1572-08-13",
    "value": 0
  },
  {
    "date": "1572-08-27",
    "value": 0
  },
  {
    "date": "1572-08-31",
    "value": 1290
  },
  {
    "date": "1572-09-10",
    "value": 0
  },
  {
    "date": "1572-10-23",
    "value": 868
  },
  {
    "date": "1572-10-29",
    "value": 0
  },
  {
    "date": "1572-11-02",
    "value": 0
  },
  {
    "date": "1572-11-04",
    "value": 1224
  },
  {
    "date": "1572-11-20",
    "value": 204
  },
  {
    "date": "1572-11-21",
    "value": 4103
  },
  {
    "date": "1572-11-27",
    "value": 1320
  },
  {
    "date": "1572-11-30",
    "value": 0
  },
  {
    "date": "1572-12-01",
    "value": 2252
  },
  {
    "date": "1572-12-07",
    "value": 1828
  },
  {
    "date": "1572-12-15",
    "value": 0
  },
  {
    "date": "1572-12-17",
    "value": 0
  },
  {
    "date": "1572-12-28",
    "value": 0
  },
  {
    "date": "1574-03-06",
    "value": 1922
  }
];   // [{date:'YYYY-MM-DD', value}, …]

const CavrianaHeatmap = () => (
  <BrowserOnly fallback={<div>Loading heat-map…</div>}>
    {() => <HeatmapOneYear />}
  </BrowserOnly>
);

const HeatmapOneYear = () => {
  const [yearIx, setYearIx] = useState(0); // Default to first year in YEARS array
  const [err, setErr] = useState(null);
  const [busy, setBusy] = useState(true);
  const calRef = useRef(null); // To hold the CalHeatmap instance

  useEffect(() => {
    setBusy(true);
    setErr(null);

    const newCal = new CalHeatmap();

    const calendarDiv = document.getElementById('cav-calendar');
    if (calendarDiv) {
      calendarDiv.innerHTML = ''; 
    }
    const legendDiv = document.getElementById('cav-legend');
    if (legendDiv) {
      legendDiv.innerHTML = ''; 
    }

    const PLUGINS = [
      [
        LegendLite,
        {
          itemSelector: '#cav-legend', 
          width: 170,
        },
      ],
      [
        Tooltip,
        {
          text: (ts, val, dayjsDate) =>
            val
              ? `${dayjsDate.format('D MMMM YYYY')}: ${val} words`
              : 'No letters on this day',
        },
      ],
    ];

    const currentYear = YEARS[yearIx];
    const yearRows = rows
      .filter(r => r.date.startsWith(String(currentYear)))
      .map(r => ({ date: new Date(r.date).getTime() / 1000, value: r.value }));

    const maxValue = yearRows.length
      ? Math.max(...yearRows.map(r => r.value))
      : 1; 

    newCal
      .paint(
        {
          itemSelector: '#cav-calendar', 
          date: { start: new Date(currentYear, 0, 1), timezone: 'utc' },
          range: 1,
          domain: {
            type: 'year',
            gutter: 10,
            label: { text: ts => new Date(ts).getUTCFullYear(), position: 'top' }, 
          },
          subDomain: {
            type: 'day',
            width: 11,
            height: 11,
            gutter: 2,
            radius: 2,
          },
          data: { source: yearRows, x: 'date', y: 'value', type: 'json' },
          scale: {
            color: {
              type: 'quantize',
              scheme: 'Spectral', 
              domain: [0, maxValue],
            },
          },
        },
        PLUGINS
      )
      .then(() => {
        setBusy(false);
        calRef.current = newCal;
      })
      .catch(e => {
        console.error("CalHeatmap paint error:", e);
        setErr(e.message || "Unknown error painting heatmap.");
        setBusy(false);
      });

    return () => {
      newCal?.destroy()
        .then(() => {
          if (calendarDiv) calendarDiv.innerHTML = '';
          if (legendDiv) legendDiv.innerHTML = '';
        })
        .catch(destroyError => {
          // console.error(`Error destroying CalHeatmap instance for ${currentYear}:`, destroyError);
        });
      calRef.current = null; 
    };
  }, [yearIx]); 

  if (err) {
    return (
      <div className="cavriana-heatmap">
        <h2>Cavriana Letter-Writing Activity – {YEARS[yearIx]}</h2>
        <p style={{ color: 'red' }}>Heat-map error: {err}</p>
        <p>Data for {YEARS[yearIx]}: {JSON.stringify(rows.filter(r => r.date.startsWith(String(YEARS[yearIx]))))}</p>
      </div>
    );
  }

  const prev = () => yearIx > 0 && setYearIx(yearIx - 1);
  const next = () => yearIx < YEARS.length - 1 && setYearIx(yearIx + 1);
  const jumpTo = i => setYearIx(i);

  return (
    <div className="cavriana-heatmap">
      <h2>Cavriana Letter-Writing Activity – {YEARS[yearIx]}</h2>

      <div className="year-selector">
        {YEARS.map((y, i) => (
          <button
            key={y}
            onClick={() => jumpTo(i)}
            className={`year-button ${yearIx === i ? 'active' : ''}`} 
          >
            {y}
          </button>
        ))}
      </div>

      {/* Keyed wrapper div starts here */}
      <div key={yearIx} className="heatmap-instance-wrapper">
        {busy && <p>Loading heatmap for {YEARS[yearIx]}…</p>}
        <div id="cav-calendar" style={{ minHeight: 200 }} /> 
        <div id="cav-legend" style={{ marginTop: 6 }} />
      </div>
      {/* Keyed wrapper div ends here */}

      <div style={{ marginTop: 8, textAlign: 'center' }}>
        <button onClick={prev} disabled={yearIx === 0}>
          ◀︎
        </button>
        <span style={{ margin: '0 1rem' }}>{YEARS[yearIx]}</span>
        <button onClick={next} disabled={yearIx === YEARS.length - 1}>
          ▶︎
        </button>
      </div>
    </div>
  );
};

export default CavrianaHeatmap;
