import React, {useEffect, useState, useRef} from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import CalHeatmap from 'cal-heatmap';
import * as d3 from 'd3';

/* ── list every year you have data for ─────────────────────────────── */
const YEARS = [1568, 1569, 1570, 1571];

const CavrianaHeatmap = () => (
  <BrowserOnly fallback={<div>Loading heat-map…</div>}>
    {() => <HeatmapOneYear />}
  </BrowserOnly>
);

/* ------------------------------------------------------------------- */
const HeatmapOneYear = () => {
  const [yearIx, setYearIx] = useState(0);
  const [err, setErr] = useState(null);
  const [busy, setBusy] = useState(true);
  const calRef = useRef(null);

  useEffect(() => {
    // Make d3 available globally
    if (!window.d3) {
      window.d3 = d3;
    }
    
    // Clean up previous instance
    if (calRef.current) {
      calRef.current.destroy();
    }
    
    // Create new instance
    calRef.current = new CalHeatmap();
    
    // Get the data for the current year
    const currentYear = YEARS[yearIx];
    const filteredData = rows.filter(item => item.date.startsWith(currentYear));
    
    // Convert to object format for Cal-Heatmap
    const dataObject = {};
    filteredData.forEach(item => {
      dataObject[item.date] = item.value;
    });
    
    // Initialize the heat map
    calRef.current.paint({
      itemSelector: '#cav-calendar',
      
      date: {
        start: new Date(currentYear, 0, 1),
        timezone: 'utc'
      },
      
      range: 1,
      
      domain: {
        type: 'year',
        gutter: 10,
        label: { text: year => year.getFullYear() }
      },
      
      subDomain: {
        type: 'day', 
        width: 11, 
        height: 11, 
        gutter: 2, 
        radius: 2
      },
      
      data: {
        source: dataObject,
        type: 'json',
      },
      
      scale: {
        color: {
          type: 'quantize',
          range: ['#f7fcf5', '#d3eecd', '#a9ddb7', '#73c9a1', '#43b78b', '#22a07b', '#187c6c', '#135e58', '#0d4042', '#03171d'],
          domain: [0, 5380]
        }
      },
      
      legend: {
        show: true,
        itemSelector: '#cav-legend',
        position: 'bottom'
      },
      
      tooltip: {
        enabled: true,
        text: (date, value) => {
          if (!value) return 'No letters on this day';
          
          const dateStr = new Date(date).toLocaleDateString('en-GB', {
            day: 'numeric', 
            month: 'long', 
            year: 'numeric'
          });
          
          return `${dateStr}: ${value} words`;
        }
      }
    })
    .then(() => setBusy(false))
    .catch(e => { 
      console.error('Cal-Heatmap error:', e);
      setErr(e.message); 
      setBusy(false); 
    });

    return () => {
      if (calRef.current) {
        calRef.current.destroy();
      }
    };
  }, [yearIx]);

  /* Error display */
  if (err) return (
    <div className="cavriana-heatmap">
      <h2>Cavriana Letter-Writing Activity – {YEARS[yearIx]}</h2>
      <p style={{color:'red'}}>Heat-map error: {err}</p>
      <pre style={{fontSize: '12px', color: '#666', maxHeight: '200px', overflow: 'auto'}}>
        {JSON.stringify({
          yearIndex: yearIx, 
          selectedYear: YEARS[yearIx],
          calHeatmapGlobal: !!window.CalHeatmap,
          d3Global: !!window.d3
        }, null, 2)}
      </pre>
    </div>
  );

  /* Navigation handlers */
  const prev = () => yearIx > 0 && setYearIx(yearIx-1);
  const next = () => yearIx < YEARS.length-1 && setYearIx(yearIx+1);

  return (
    <div className="cavriana-heatmap">
      <h2>Cavriana Letter-Writing Activity – {YEARS[yearIx]}</h2>

      {busy && <p>Loading…</p>}
      <div id="cav-calendar" style={{minHeight:150}} />
      <div id="cav-legend" style={{marginTop:6}} />

      <div style={{marginTop:8, textAlign:'center'}}>
        <button onClick={prev} disabled={yearIx === 0}>◀︎</button>
        <span style={{margin:'0 1rem'}}>{YEARS[yearIx]}</span>
        <button onClick={next} disabled={yearIx === YEARS.length-1}>▶︎</button>
      </div>
    </div>
  );
};

/* Data rows from Python script */
const rows = [
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
    "value": 614
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
    "value": 859
  },
  {
    "date": "1570-11-02",
    "value": 894
  },
  {
    "date": "1570-11-02",
    "value": 864
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
    "date": "1571-07-15",
    "value": 326
  }
];

export default CavrianaHeatmap;