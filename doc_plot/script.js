document.getElementById('plot-button').addEventListener('click', () => {
  const ropMin = parseFloat(document.getElementById('rop-min').value);
  const ropMax = parseFloat(document.getElementById('rop-max').value);
  const rpmMin = parseFloat(document.getElementById('rpm-min').value);
  const rpmMax = parseFloat(document.getElementById('rpm-max').value);
  const docValue = parseFloat(document.getElementById('doc-value').value);

  const rpm = [];
  const rop = [];
  const doc = [];

  for (let i = 0; i <= 100; i++) {
    rpm.push(rpmMin + ((rpmMax - rpmMin) * i) / 100);
    rop.push(ropMin + ((ropMax - ropMin) * i) / 100);
  }

  for (let i = 0; i <= 100; i++) {
    const row = [];
    for (let j = 0; j <= 100; j++) {
      const docVal = rpm[j] !== 0 ? (rop[i] * 12) / (rpm[j] * 60) : 1000;
      row.push(docVal);
    }
    doc.push(row);
  }

  const data = [
    {
      x: rpm,
      y: rop,
      z: doc,
      type: 'contour',
      colorscale: [
        [0, 'yellow'],
        [docValue / (Math.max(...doc.flat()) || 1), 'limegreen'],
        [1, 'limegreen'],
      ],
      contours: {
        start: 0,
        end: Math.max(...doc.flat()) || 1,
        size: 0.05,
        showlines: true,
        coloring: 'fill',
        showlabels: true,
      },
    },
  ];

  const layout = {
    title: `DOC Chart (DOC = ${docValue} in/rev)`,
    xaxis: { title: 'Rotary Speed (RPM)' },
    yaxis: { title: 'Rate of Penetration (ft/hr)' },
    width: 700,
    height: 500,
    annotations: [
      {
        x: (rpmMax - rpmMin) * 0.3 + rpmMin,
        y: (ropMax - ropMin) * 0.8 + ropMin,
        text: 'DOC feature engaged<br>Adjust RPM, WOB, & Flow to Minimize:<br>-MSE (Whirl, balling, dysfunction) and<br>-Torque Variation (Stick-slip)',
        showarrow: false,
        font: { size: 16 },
        bgcolor: 'limegreen',
        bordercolor: 'black',
        borderwidth: 1,
      },
      {
        x: (rpmMax - rpmMin) * 0.7 + rpmMin,
        y: (ropMax - ropMin) * 0.2 + ropMin,
        text: 'DOC feature not engaged<br>Increase WOB',
        showarrow: false,
        font: { size: 16 },
        bgcolor: 'yellow',
        bordercolor: 'black',
        borderwidth: 1,
      },
    ],
  };

  Plotly.newPlot('plot', data, layout);
});
