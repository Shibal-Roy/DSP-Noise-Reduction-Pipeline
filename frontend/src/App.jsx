import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
  const [cutoff, setCutoff] = useState(2.0);
  const [order, setOrder] = useState(4);
  const [metrics, setMetrics] = useState({ snr_db: 0, improvement_percent: 0 });
  const [chartData, setChartData] = useState([]);

  // This function reaches across the bridge to your Python FastAPI server
  const fetchDSPData = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/process?rate=20&cutoff=${cutoff}&order=${order}`);
      const data = await response.json();
      
      setMetrics(data.metrics);
      
      // Recharts needs the data formatted as an array of objects
      const formattedData = data.graph_data.time.map((t, index) => ({
        time: t.toFixed(2),
        rawVoltage: data.graph_data.raw[index],
        cleanVoltage: data.graph_data.clean[index]
      }));
      setChartData(formattedData);
    } catch (error) {
      console.error("Bridge failure: Python server might be down.", error);
    }
  };

  // Run the fetch whenever the sliders change
  useEffect(() => {
    fetchDSPData();
  }, [cutoff, order]);

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif', backgroundColor: '#f4f4f9', minHeight: '100vh' }}>
      <h1 style={{ color: '#333' }}>⚙️ Industrial DSP Control Panel</h1>
      
      {/* KPI Cards Section */}
      <div style={{ display: 'flex', gap: '20px', marginBottom: '30px' }}>
        <div style={cardStyle}>
          <h3 style={{ margin: 0, color: '#666' }}>Target Frequency</h3>
          <h2 style={{ margin: '10px 0', color: '#007bff' }}>1.5 Hz</h2>
          <p style={{ margin: 0, fontSize: '12px', color: '#888' }}>(Biometric Baseline)</p>
        </div>
        <div style={cardStyle}>
          <h3 style={{ margin: 0, color: '#666' }}>Calculated SNR</h3>
          <h2 style={{ margin: '10px 0', color: metrics.snr_db > 0 ? '#28a745' : '#dc3545' }}>
            {metrics.snr_db} dB
          </h2>
          <p style={{ margin: 0, fontSize: '12px', color: '#888' }}>Signal vs Noise Power</p>
        </div>
        <div style={cardStyle}>
          <h3 style={{ margin: 0, color: '#666' }}>Static Destroyed</h3>
          <h2 style={{ margin: '10px 0', color: '#6f42c1' }}>{metrics.improvement_percent}%</h2>
          <p style={{ margin: 0, fontSize: '12px', color: '#888' }}>Variance Reduction</p>
        </div>
      </div>

      {/* Control Sliders Section */}
      <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', marginBottom: '30px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
        <div style={{ marginBottom: '20px' }}>
          <label style={{ fontWeight: 'bold', marginRight: '15px' }}>Cutoff Frequency: {cutoff} Hz</label>
          <input 
            type="range" min="0.5" max="9.0" step="0.1" 
            value={cutoff} 
            onChange={(e) => setCutoff(parseFloat(e.target.value))} 
            style={{ width: '300px' }}
          />
        </div>
        <div>
          <label style={{ fontWeight: 'bold', marginRight: '55px' }}>Filter Order: {order}</label>
          <input 
            type="range" min="1" max="8" step="1" 
            value={order} 
            onChange={(e) => setOrder(parseInt(e.target.value))} 
            style={{ width: '300px' }}
          />
        </div>
      </div>

      {/* The Recharts Graph */}
      <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
        <h3 style={{ marginTop: 0 }}>Live Time-Domain Analysis</h3>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" label={{ value: 'Time (s)', position: 'insideBottomRight', offset: -5 }} />
            <YAxis label={{ value: 'Voltage', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend verticalAlign="top" height={36}/>
            <Line type="monotone" dataKey="rawVoltage" name="Raw Sensor Data (Interference)" stroke="#ff4d4f" dot={false} strokeWidth={2} />
            <Line type="monotone" dataKey="cleanVoltage" name="Filtered Output (Target)" stroke="#1890ff" dot={false} strokeWidth={3} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

// Simple styling for the KPI cards
const cardStyle = {
  backgroundColor: 'white',
  padding: '20px',
  borderRadius: '8px',
  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  flex: 1,
  textAlign: 'center'
};

export default App;
