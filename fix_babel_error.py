import os

# Clean React App.jsx fallback code
clean_app_code = '''import React, { useState, useEffect } from "react";

export default function App() {
  const [time, setTime] = useState(new Date().toLocaleTimeString());
  const [logs, setLogs] = useState([
    "[SYSTEM_INIT] Neural core loaded successfully.",
    "[SECURITY] Quantum encryption handshakes established.",
    "[STATUS] All primary modules operating at 100% efficiency."
  ]);
  const [command, setCommand] = useState("");
  const [coreStatus, setCoreStatus] = useState("NOMINAL");

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date().toLocaleTimeString()), 1000);
    return () => clearInterval(timer);
  }, []);

  const handleSendCommand = (e) => {
    e.preventDefault();
    if (!command.trim()) return;
    
    setLogs((prev) => [...prev, `[USER_EXEC] ${command}`, `[JARVIS] Command "${command}" executed.`]);
    setCommand("");
  };

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#030712',
      color: '#00f3ff',
      fontFamily: 'monospace',
      padding: '2rem',
      boxSizing: 'border-box'
    }}>
      <header style={{
        borderBottom: '1px solid rgba(0, 243, 255, 0.3)',
        paddingBottom: '1rem',
        marginBottom: '2rem',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '1.8rem', letterSpacing: '2px', textShadow: '0 0 10px #00f3ff' }}>
            JARVIS // ULTIMATE AUTONOMOUS SYSTEM
          </h1>
          <p style={{ margin: '0.4rem 0 0 0', color: '#00c3ff', fontSize: '0.8rem' }}>Cybernetic Neural Core v4.8.2</p>
        </div>
        <div style={{ textAlign: 'right', fontSize: '0.85rem' }}>
          <div>CLOCK: <strong>{time}</strong></div>
          <div style={{ color: '#10b981', marginTop: '0.2rem' }}>STATUS: ● {coreStatus}</div>
        </div>
      </header>

      <main style={{
        display: 'grid',
        gridTemplateColumns: '1fr 3fr',
        gap: '1.5rem'
      }}>
        <aside style={{
          backgroundColor: '#061224',
          border: '1px solid rgba(0, 243, 255, 0.3)',
          borderRadius: '8px',
          padding: '1.5rem'
        }}>
          <h2 style={{ fontSize: '1rem', borderBottom: '1px solid rgba(0, 243, 255, 0.2)', paddingBottom: '0.5rem', marginTop: 0 }}>
            DIAGNOSTICS
          </h2>
          <p style={{ fontSize: '0.8rem', color: '#64748b' }}>Neural Load: 24%</p>
          <p style={{ fontSize: '0.8rem', color: '#64748b' }}>Quantum RAM: 14.2 / 64 TB</p>
          <p style={{ fontSize: '0.8rem', color: '#10b981' }}>Latency: 0.12 ms</p>
        </aside>

        <section style={{
          backgroundColor: '#061224',
          border: '1px solid rgba(0, 243, 255, 0.3)',
          borderRadius: '8px',
          padding: '1.5rem',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between'
        }}>
          <div style={{ overflowY: 'auto', maxHeight: '400px', fontSize: '0.85rem' }}>
            {logs.map((log, idx) => (
              <div key={idx} style={{ marginBottom: '0.5rem', color: log.includes('USER') ? '#f59e0b' : '#00f3ff' }}>
                &gt; {log}
              </div>
            ))}
          </div>

          <form onSubmit={handleSendCommand} style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
            <input
              type="text"
              value={command}
              onChange={(e) => setCommand(e.target.value)}
              placeholder="Execute command or query JARVIS core..."
              style={{
                flex: 1,
                backgroundColor: '#030712',
                border: '1px solid rgba(0, 243, 255, 0.4)',
                borderRadius: '4px',
                padding: '0.6rem 1rem',
                color: '#00f3ff',
                fontFamily: 'monospace',
                outline: 'none'
              }}
            />
            <button type="submit" style={{
              backgroundColor: '#00f3ff',
              color: '#030712',
              fontWeight: 'bold',
              border: 'none',
              borderRadius: '4px',
              padding: '0.6rem 1.2rem',
              cursor: 'pointer'
            }}>
              EXECUTE
            </button>
          </form>
        </section>
      </main>
    </div>
  );
}
'''

# Restore Clean App.jsx
with open("frontend/src/App.jsx", "w", encoding="utf-8") as f:
    f.write(clean_app_code)

print("[SUCCESS] Restored Clean frontend/src/App.jsx file!")