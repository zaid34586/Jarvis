import React, { useState, useEffect } from 'react';

export default function App() {
  const [command, setCommand] = useState('');
  const [logs, setLogs] = useState([
    { id: 1, type: 'system', text: 'JARVIS Autonomous Core v4.2 Initialized.' },
    { id: 2, type: 'system', text: 'Server Health Monitoring Module active.' }
  ]);
  const [isProcessing, setIsProcessing] = useState(false);

  // Simulated server metrics
  const [metrics, setMetrics] = useState({
    cpuUsage: 24,
    ramUsage: 48,
    serverTemp: 38,
    latency: 14,
    uptime: '99.98%',
    diskUsage: 62,
    status: 'OPTIMAL'
  });

  // Pulse effect simulation for realistic live dashboard
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => ({
        ...prev,
        cpuUsage: Math.floor(20 + Math.random() * 15),
        ramUsage: Math.floor(45 + Math.random() * 6),
        serverTemp: Math.floor(37 + Math.random() * 3),
        latency: Math.floor(12 + Math.random() * 5)
      }));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleCommandSubmit = async (e) => {
    e.preventDefault();
    if (!command.trim()) return;

    const userCmd = command;
    setCommand('');
    setLogs(prev => [...prev, { id: Date.now(), type: 'user', text: `> ${userCmd}` }]);
    setIsProcessing(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: userCmd })
      });
      const data = await response.json();
      setLogs(prev => [
        ...prev, 
        { id: Date.now() + 1, type: 'response', text: data.result || data.message || 'Command executed successfully.' }
      ]);
    } catch (error) {
      setLogs(prev => [
        ...prev, 
        { id: Date.now() + 1, type: 'error', text: `Execution failed: ${error.message}` }
      ]);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div style={{ backgroundColor: '#030712', color: '#00f3ff', fontFamily: 'monospace', minHeight: '100vh', padding: '20px', paddingBottom: '90px', boxSizing: 'border-box' }}>
      
      {/* Dashboard Header */}
      <header style={{ borderBottom: '1px solid #00f3ff44', paddingBottom: '15px', marginBottom: '25px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '24px', letterSpacing: '2px', textTransform: 'uppercase' }}>
            JARVIS // AUTONOMOUS CORE
          </h1>
          <span style={{ fontSize: '12px', opacity: 0.7 }}>SYS_VER: 4.2.0-STABLE | NODE: 127.0.0.1</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', border: '1px solid #00f3ff66', padding: '4px 12px', borderRadius: '4px' }}>
          <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#00f3ff', boxShadow: '0 0 8px #00f3ff' }}></span>
          CORE ONLINE
        </div>
      </header>

      {/* Main Grid */}
      <main style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px', marginBottom: '25px' }}>
        
        {/* Server Health Status Widget */}
        <section style={{ backgroundColor: '#081226', border: '1px solid #00f3ff44', borderRadius: '6px', padding: '20px', boxShadow: '0 0 15px rgba(0,243,255,0.05)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #00f3ff22', paddingBottom: '10px', marginBottom: '15px' }}>
            <h2 style={{ margin: 0, fontSize: '16px', letterSpacing: '1px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontSize: '18px' }}>⚡</span> SERVER HEALTH STATUS
            </h2>
            <span style={{ fontSize: '11px', backgroundColor: '#00f3ff22', color: '#00f3ff', padding: '2px 8px', borderRadius: '3px', border: '1px solid #00f3ff44' }}>
              {metrics.status}
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {/* CPU Usage Bar */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
                <span>CPU LOAD</span>
                <span>{metrics.cpuUsage}%</span>
              </div>
              <div style={{ width: '100%', backgroundColor: '#030712', height: '8px', borderRadius: '4px', overflow: 'hidden', border: '1px solid #00f3ff33' }}>
                <div style={{ width: `${metrics.cpuUsage}%`, backgroundColor: '#00f3ff', height: '100%', transition: 'width 0.5s ease', boxShadow: '0 0 8px #00f3ff' }}></div>
              </div>
            </div>

            {/* RAM Usage Bar */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
                <span>MEMORY ALLOCATION</span>
                <span>{metrics.ramUsage}%</span>
              </div>
              <div style={{ width: '100%', backgroundColor: '#030712', height: '8px', borderRadius: '4px', overflow: 'hidden', border: '1px solid #00f3ff33' }}>
                <div style={{ width: `${metrics.ramUsage}%`, backgroundColor: '#00f3ff', height: '100%', transition: 'width 0.5s ease', boxShadow: '0 0 8px #00f3ff' }}></div>
              </div>
            </div>

            {/* Metrics Quick Stats */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginTop: '5px' }}>
              <div style={{ backgroundColor: '#030712', padding: '10px', borderRadius: '4px', border: '1px solid #00f3ff22' }}>
                <div style={{ fontSize: '10px', opacity: 0.6 }}>CORE TEMP</div>
                <div style={{ fontSize: '16px', fontWeight: 'bold', marginTop: '2px' }}>{metrics.serverTemp} °C</div>
              </div>
              <div style={{ backgroundColor: '#030712', padding: '10px', borderRadius: '4px', border: '1px solid #00f3ff22' }}>
                <div style={{ fontSize: '10px', opacity: 0.6 }}>LATENCY</div>
                <div style={{ fontSize: '16px', fontWeight: 'bold', marginTop: '2px' }}>{metrics.latency} ms</div>
              </div>
              <div style={{ backgroundColor: '#030712', padding: '10px', borderRadius: '4px', border: '1px solid #00f3ff22' }}>
                <div style={{ fontSize: '10px', opacity: 0.6 }}>STORAGE</div>
                <div style={{ fontSize: '16px', fontWeight: 'bold', marginTop: '2px' }}>{metrics.diskUsage}%</div>
              </div>
              <div style={{ backgroundColor: '#030712', padding: '10px', borderRadius: '4px', border: '1px solid #00f3ff22' }}>
                <div style={{ fontSize: '10px', opacity: 0.6 }}>UPTIME</div>
                <div style={{ fontSize: '16px', fontWeight: 'bold', marginTop: '2px' }}>{metrics.uptime}</div>
              </div>
            </div>
          </div>
        </section>

        {/* System Terminal Log Stream */}
        <section style={{ backgroundColor: '#081226', border: '1px solid #00f3ff44', borderRadius: '6px', padding: '20px', display: 'flex', flexDirection: 'column', height: '280px' }}>
          <h2 style={{ margin: 0, fontSize: '16px', letterSpacing: '1px', borderBottom: '1px solid #00f3ff22', paddingBottom: '10px', marginBottom: '10px' }}>
            SYSTEM LOG STREAM
          </h2>
          <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '12px' }}>
            {logs.map(log => (
              <div key={log.id} style={{ 
                color: log.type === 'error' ? '#ff4444' : log.type === 'user' ? '#ffffff' : '#00f3ff',
                opacity: log.type === 'system' ? 0.8 : 1
              }}>
                {log.text}
              </div>
            ))}
            {isProcessing && <div style={{ opacity: 0.5 }}>Processing payload...</div>}
          </div>
        </section>
      </main>

      {/* Mandatory Fixed Command Input Bar */}
      <div style={{ 
        position: 'fixed', 
        bottom: 0, 
        left: 0, 
        right: 0, 
        backgroundColor: '#050c1e', 
        borderTop: '1px solid #00f3ff66', 
        padding: '12px 20px', 
        boxShadow: '0 -5px 25px rgba(0,0,0,0.8)',
        zIndex: 1000 
      }}>
        <form onSubmit={handleCommandSubmit} style={{ display: 'flex', gap: '12px', maxWidth: '1200px', margin: '0 auto', alignItems: 'center' }}>
          <span style={{ color: '#00f3ff', fontWeight: 'bold', fontSize: '14px' }}>JARVIS&gt;</span>
          <input 
            type="text" 
            value={command} 
            onChange={(e) => setCommand(e.target.value)} 
            placeholder="Execute system command or directive..."
            style={{ 
              flex: 1, 
              backgroundColor: '#030712', 
              color: '#00f3ff', 
              border: '1px solid #00f3ff44', 
              borderRadius: '4px', 
              padding: '10px 14px', 
              fontFamily: 'monospace', 
              fontSize: '14px', 
              outline: 'none' 
            }}
          />
          <button 
            type="submit" 
            disabled={isProcessing}
            style={{ 
              backgroundColor: '#00f3ff', 
              color: '#030712', 
              border: 'none', 
              borderRadius: '4px', 
              padding: '10px 20px', 
              fontFamily: 'monospace', 
              fontWeight: 'bold', 
              cursor: isProcessing ? 'not-allowed' : 'pointer',
              opacity: isProcessing ? 0.6 : 1,
              letterSpacing: '1px'
            }}
          >
            {isProcessing ? 'BUSY' : 'EXECUTE'}
          </button>
        </form>
      </div>

    </div>
  );
}