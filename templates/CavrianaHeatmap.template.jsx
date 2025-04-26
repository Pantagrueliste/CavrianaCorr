import React, {useEffect, useState} from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import CalHeatmap from 'cal-heatmap';

const CavrianaHeatmap = () => (
  <BrowserOnly fallback={<div>Loading heat-map…</div>}>
    {() => <HeatmapContent />}
  </BrowserOnly>
);

const HeatmapContent = () => {
  const [err , setErr ] = useState(null);
  const [busy, setBusy] = useState(true);

  useEffect(() => {
    const cal  = new CalHeatmap();
    const rows = /* __DATA_PLACEHOLDER__ */;   // ← data injected by Python

    cal.paint({
      itemSelector : '#cav-calendar',
      legend       : {itemSelector: '#cav-legend', position: 'bottom'},

      date   : {start: new Date(1568, 0, 1)},
      range  : 4,
      domain : {type: 'year', gutter: 10},
      subDomain: {type: 'day', width: 11, height: 11, gutter: 2, radius: 2},

      data  : {type: 'json', source: rows, x: 'date', y: 'value'},

      scale : {color: {type: 'quantize', scheme: 'Spectral', domain: [278, 5380]}},

      tooltip: {
        enabled: true,
        text: (v, t) =>
          v
            ? `${new Date(t).toLocaleDateString('en-GB',
               {day:'numeric', month:'long', year:'numeric'})}: ${v} words`
            : 'No letters on this day',
      },
    })
    .then(() => setBusy(false))
    .catch(e  => { setErr(e.message); setBusy(false); });

    return () => cal.destroy();
  }, []);

  if (err) return <p style={{color:'red'}}>Heat-map error: {err}</p>;

  return (
    <div className="cavriana-heatmap">
      <h2>Cavriana Letter-Writing Activity</h2>
      {busy && <p>Loading…</p>}
      <div id="cav-calendar" style={{minHeight:150}} />
      <div id="cav-legend"   style={{marginTop:6}} />
    </div>
  );
};

export default CavrianaHeatmap;