/* templates/CavrianaHeatmap.template.jsx
   ---------------------------------------------------------------
   React component produced by scripts/generate_heatmap.py.
   Renders a single-year GitHub-style heat-map with arrow navigation.
*/

import React, { useEffect, useState, useRef } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import CalHeatmap from 'cal-heatmap';
import * as d3 from 'd3';

/* years present in the corpus – overwritten by generate_heatmap.py */
const YEARS = [1568, 1569, 1570, 1571];

/* rows injected by the build script
   [{ date: 'YYYY-MM-DD', value: <word-count> }, … ]                */
const rows = /* __DATA_PLACEHOLDER__ */;

const CavrianaHeatmap = () => (
  <BrowserOnly fallback={<div>Loading heat-map…</div>}>
    {() => <HeatmapOneYear />}
  </BrowserOnly>
);

const HeatmapOneYear = () => {
  const [yearIx, setYearIx] = useState(0);
  const [err,    setErr]    = useState(null);
  const [busy,   setBusy]   = useState(true);
  const calRef              = useRef(null);

  useEffect(() => {
    /* Cal-Heatmap’s tooltip helper expects d3 on window */
    if (!window.d3) window.d3 = d3;

    /* destroy any previous instance */
    calRef.current?.destroy();
    calRef.current = new CalHeatmap();

    const currentYear = YEARS[yearIx];

    /* keep only the rows for the selected year */
    const yearRows = rows.filter(r => r.date.startsWith(currentYear));
    const maxValue = yearRows.length
      ? Math.max(...yearRows.map(r => r.value))
      : 0;

    calRef.current
      .paint({
        itemSelector: '#cav-calendar',

        date : { start: new Date(currentYear, 0, 1), timezone: 'utc' },
        range: 1,                               // one domain → one year

        domain: {
          type  : 'year',
          gutter: 10,
          /* Cal-Heatmap passes a Unix-ms timestamp; convert to Date */
          label : { text: ts => new Date(ts).getUTCFullYear() },
        },

        subDomain: {
          type  : 'day',
          width : 11,
          height: 11,
          gutter: 2,
          radius: 2,
        },

        /* feed the raw rows, tell Cal-Heatmap which fields to use */
        data: { source: yearRows, x: 'date', y: 'value', type: 'json' },

        scale: {
          color: {
            type  : 'quantize',
            scheme: 'Spectral',
            domain: [0, maxValue || 1],         // avoid zero-range crash
          },
        },

        legend: {
          show        : true,
          itemSelector: '#cav-legend',
          position    : 'bottom',
        },

        tooltip: {
          enabled: true,
          text   : (date, value) =>
            value
              ? `${new Date(date).toLocaleDateString('en-GB', {
                  day  : 'numeric',
                  month: 'long',
                  year : 'numeric',
                })}: ${value} words`
              : 'No letters on this day',
        },
      })
      .then(() => setBusy(false))
      .catch(e => {
        console.error('Cal-Heatmap error:', e);
        setErr(e.message);
        setBusy(false);
      });

    return () => calRef.current?.destroy();
  }, [yearIx]);

  /* ── error banner ───────────────────────────────────────────── */
  if (err) {
    return (
      <div className="cavriana-heatmap">
        <h2>Cavriana Letter-Writing Activity – {YEARS[yearIx]}</h2>
        <p style={{ color: 'red' }}>Heat-map error: {err}</p>
      </div>
    );
  }

  /* ── navigation helpers ─────────────────────────────────────── */
  const prev   = () => yearIx > 0 && setYearIx(yearIx - 1);
  const next   = () => yearIx < YEARS.length - 1 && setYearIx(yearIx + 1);
  const select = i => setYearIx(i);

  return (
    <div className="cavriana-heatmap">
      <h2>Cavriana Letter-Writing Activity – {YEARS[yearIx]}</h2>

      {/* jump directly to a year */}
      <div className="year-selector">
        {YEARS.map((y, i) => (
          <button
            key={y}
            onClick={() => select(i)}
            className={`year-button ${yearIx === i ? 'active' : ''}`}
          >
            {y}
          </button>
        ))}
      </div>

      {busy && <p>Loading…</p>}
      <div id="cav-calendar" style={{ minHeight: 150 }} />
      <div id="cav-legend"   style={{ marginTop: 6 }} />

      {/* previous / next arrows */}
      <div style={{ marginTop: 8, textAlign: 'center' }}>
        <button onClick={prev} disabled={yearIx === 0}>◀︎</button>
        <span style={{ margin: '0 1rem' }}>{YEARS[yearIx]}</span>
        <button onClick={next} disabled={yearIx === YEARS.length - 1}>▶︎</button>
      </div>
    </div>
  );
};

export default CavrianaHeatmap;
