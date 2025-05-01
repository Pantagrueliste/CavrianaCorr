/* templates/CavrianaHeatmap.template.jsx
   ---------------------------------------------------------------
   React component produced by scripts/generate_heatmap.py.
   Renders a single-year GitHub-style heat-map with arrow navigation.
*/

import React, { useEffect, useState, useRef } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

import CalHeatmap  from 'cal-heatmap';
import Legend      from 'cal-heatmap/plugins/Legend';
import Tooltip     from 'cal-heatmap/plugins/Tooltip';
import 'cal-heatmap/cal-heatmap.css';

import * as d3 from 'd3';

/* overwritten by generate_heatmap.py */
const YEARS = [1568, 1569, 1570, 1571];
const rows  = /* __DATA_PLACEHOLDER__ */;   // [{date:'YYYY-MM-DD', value}, …]

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
    if (!window.d3) window.d3 = d3;

    calRef.current?.destroy();
    calRef.current = new CalHeatmap();

    /* register plugins ----------------------------------------------------- */
    const PLUGINS = [
      [Legend , { itemSelector: '#cav-legend', position: 'bottom' }],
      [Tooltip, {}],
    ];

    const currentYear = YEARS[yearIx];

    /* keep rows of this year and turn ISO date → epoch-seconds -------------- */
    const yearRows = rows
      .filter(r => r.date.startsWith(currentYear))
      .map(r => ({ date: Date.parse(r.date) / 1000, value: r.value }));

    const maxValue = yearRows.length ? Math.max(...yearRows.map(r => r.value)) : 1;

    calRef.current
      .paint({
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

        data : { source: yearRows, x: 'date', y: 'value', type: 'json' },

        scale: {
          color: {
            type  : 'quantize',
            scheme: 'Spectral',
            domain: [0, maxValue],
          },
        },
      }, PLUGINS)                   // ← plugin array passed here
      .then(() => setBusy(false))
      .catch(e => { setErr(e.message); setBusy(false); });

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

  /* navigation ------------------------------------------------------------- */
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
