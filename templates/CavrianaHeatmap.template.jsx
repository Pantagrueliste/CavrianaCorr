import React, {useEffect, useState} from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import CalHeatmap from 'cal-heatmap';

/* ── list every year you have data for ─────────────────────────────── */
const YEARS = [1567, 1568, 1569, 1570];

const CavrianaHeatmap = () => (
  <BrowserOnly fallback={<div>Loading heat-map…</div>}>
    {() => <HeatmapOneYear />}
  </BrowserOnly>
);

/* ------------------------------------------------------------------- */
const HeatmapOneYear = () => {
  const [yearIx, setYearIx] = useState(0);   // 0 → YEARS[0]
  const [err , setErr ] = useState(null);
  const [busy, setBusy] = useState(true);

  useEffect(() => {
    const cal  = new CalHeatmap();
    const rows = /* __DATA_PLACEHOLDER__ */;           // injected by Python

    cal.paint({
      itemSelector : '#cav-calendar',
      legend       : {itemSelector:'#cav-legend', position:'bottom'},
      date   : {start: new Date(YEARS[yearIx], 0, 1)},
      range  : 1,                                      // one year
      domain : {type:'year', gutter:10},
      subDomain: {type:'day', width:11, height:11, gutter:2, radius:2},
      data  : {type:'json', source: rows, x:'date', y:'value'},
      scale : {color:{type:'quantize', scheme:'Spectral', domain:[278,5380]}},
      tooltip: {
        enabled:true,
        text:(v,t)=>
          v ? `${new Date(t).toLocaleDateString('en-GB',
               {day:'numeric', month:'long', year:'numeric'})}: ${v} words`
            : 'No letters on this day',
      },
    })
    .then(() => setBusy(false))
    .catch(e => { setErr(e.message); setBusy(false); });

    return () => cal.destroy();
  }, [yearIx]);                                        // repaint on year change

  if (err) return <p style={{color:'red'}}>Heat-map error: {err}</p>;

  /* nav handlers */
  const prev = () => yearIx && setYearIx(yearIx-1);
  const next = () => yearIx < YEARS.length-1 && setYearIx(yearIx+1);
  const selectYear = (index) => setYearIx(index);

  return (
    <div className="cavriana-heatmap">
      <h2>Cavriana Letter-Writing Activity – {YEARS[yearIx]}</h2>
      
      {/* Year selector buttons */}
      <div className="year-selector">
        {YEARS.map((year, index) => (
          <button 
            key={year}
            onClick={() => selectYear(index)}
            className={`year-button ${yearIx === index ? 'active' : ''}`}
          >
            {year}
          </button>
        ))}
      </div>
      
      {busy && <p>Loading…</p>}
      <div id="cav-calendar" style={{minHeight:150}} />
      <div id="cav-legend"   style={{marginTop:6}} />
      
      {/* Keep original prev/next navigation as an alternative */}
      <div style={{marginTop:8, textAlign:'center'}}>
        <button onClick={prev} disabled={!yearIx}>◀︎</button>
        <span style={{margin:'0 1rem'}}>{YEARS[yearIx]}</span>
        <button onClick={next} disabled={yearIx===YEARS.length-1}>▶︎</button>
      </div>
    </div>
  );
};

export default CavrianaHeatmap;            // export name unchanged
