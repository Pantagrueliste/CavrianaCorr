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

import * as d3 from 'd3';

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
    {() => <HeatmapOneYear />}
  </BrowserOnly>
);

const HeatmapOneYear = () => {
  const [yearIx, setYearIx] = useState(0);
  const [err   , setErr   ] = useState(null);
  const [busy  , setBusy  ] = useState(true);
  const calRef              = useRef(null);

  useEffect(() => {
    // Remove global D3 assignment to prevent conflicts
    calRef.current?.destroy();
    calRef.current = new CalHeatmap();

    /* --- plugins --------------------------------------------------------- */
    const PLUGINS = [
      [
        LegendLite,
        {
          itemSelector: '#cav-legend',
          width       : 170,   // px – tune to taste
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

    /* --- data for the current year -------------------------------------- */
    const currentYear = YEARS[yearIx];
    const yearRows = rows
      .filter(r => r.date.startsWith(String(currentYear)))
      .map(r => ({ date: new Date(r.date).getTime() / 1000, value: r.value }));

    const maxValue = yearRows.length
      ? Math.max(...yearRows.map(r => r.value))
      : 1;

    /* --- render ---------------------------------------------------------- */
    calRef.current
      .paint(
        {
          itemSelector: '#cav-calendar',

          date : { start: new Date(currentYear, 0, 1), timezone: 'utc' },
          range: 1,

          domain: {
            type  : 'year',
            gutter: 10,
            label : { text: ts => new Date(ts).getUTCFullYear() },
          },
          subDomain: {
            type  : 'day',
            width : 11,
            height: 11,
            gutter: 2,
            radius: 2,
          },

          data: { source: yearRows, x: 'date', y: 'value', type: 'json' },

          scale: {
            color: {
              type  : 'quantize',
              scheme: 'Spectral',
              domain: [0, maxValue],
            },
          },
        },
        PLUGINS,             // ← second argument
      )
      .then(() => setBusy(false))
      .catch(e => { console.error("CalHeatmap paint error:", e); setErr(e.message); setBusy(false); });

    return () => calRef.current?.destroy();
  }, [yearIx]);

  if (err) {
    return (
      <div className="cavriana-heatmap">
        <h2>Cavriana Letter-Writing Activity – {YEARS[yearIx]}</h2>
        <p style={{color:'red'}}>Heat-map error: {err}</p>
      </div>
    );
  }

  /* navigation ----------------------------------------------------------- */
  const prev   = () => yearIx > 0 && setYearIx(yearIx - 1);
  const next   = () => yearIx < YEARS.length - 1 && setYearIx(yearIx + 1);
  const jumpTo = i => setYearIx(i);

  return (
    <div className="cavriana-heatmap">
      <h2>Cavriana Letter-Writing Activity – {YEARS[yearIx]}</h2>

      <div className="year-selector">
        {YEARS.map((y,i) =>
          <button key={y} onClick={() => jumpTo(i)}
                  className={yearIx===i ? 'active' : ''}>{y}</button>
        )}
      </div>

      {busy && <p>Loading…</p>}
      <div id="cav-calendar" style={{minHeight:150}} />
      <div id="cav-legend"   style={{marginTop:6}} />

      <div style={{marginTop:8, textAlign:'center'}}>
        <button onClick={prev} disabled={yearIx===0}>◀︎</button>
        <span style={{margin:'0 1rem'}}>{YEARS[yearIx]}</span>
        <button onClick={next} disabled={yearIx===YEARS.length-1}>▶︎</button>
      </div>
    </div>
  );
};

export default CavrianaHeatmap;