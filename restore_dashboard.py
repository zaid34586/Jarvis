import os

clean_dashboard = '''import React, { useState, useEffect } from "react";

export default function App() {
  const [time, setTime] = useState(new Date().toLocaleTimeString());
  const [logs, setLogs] = useState([
    "[SYSTEM_INIT] Jarvis Autonomous Engine Matrix Online.",
    "[PROTECTION] Inline Style Router & Command Console Enforcement Active."
  ]);
  const [command, setCommand] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date().toLocaleTimeString()), 1000);
    return () => clearInterval(timer);
  }, []);

  const handleSendCommand = async (e) => {
    e.preventDefault();
    if (!command.trim() || loading) return;

    const userGoal = command;
    setCommand("");
    setLogs((prev) => [...prev, `[USER_EXEC] "${userGoal}"`]);
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: userGoal }),
      });
      const data = await res.json();
      setLogs((prev) => [...prev, `[JARVIS] ${data.response || "Task executed."}`]);
    } catch (err) {
      setLogs((prev) => [...prev, "[SYSTEM ERROR] Backend API disconnected."]);
    } finally {
      setLoading(false);
    }
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
        marginBottom: '1.5rem',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '1.8rem', textShadow: '0 0 10px #00f3ff' }}>
            JARVIS // AUTONOMOUS CORE CONTROL
          </h1>
          <p style={{ margin: '0.2rem 0 0 0', color: '#00c3ff', fontSize: '0.8rem' }}>
            Cybernetic Neural Interface v4.9
          </p>
        </div>
        <div style={{ textAlign: 'right', fontSize: '0.85rem' }}>
          <div>CLOCK: {time}</div>
          <div style={{ color: '#10b981', marginTop: '0.2rem' }}>● SYSTEM OPERATIONAL</div>
        </div>
      </header>

      <main style={{ display: 'grid', gridTemplateColumns: '1fr 3fr', gap: '1.5rem' }}>
        <aside style={{
          backgroundColor: '#061224',
          border: '1px solid rgba(0, 243, 255, 0.3)',
          borderRadius: '8px',
          padding: '1rem'
        }}>
          <h3 style={{ marginTop: 0, borderBottom: '1px solid rgba(0, 243, 255, 0.2)', paddingBottom: '0.5rem' }}>
            CORE METRICS
          </h3>
          <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>Neural Engine: Active</p>
          <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>Auto-Patch: Enabled</p>
          <p style={{ fontSize: '0.85rem', color: '#10b981' }}>Latency: 0.08 ms</p>
        </aside>

        <section style={{
          backgroundColor: '#061224',
          border: '1px solid rgba(0, 243, 255, 0.3)',
          borderRadius: '8px',
          padding: '1.5rem',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          minHeight: '450px'
        }}>
          <div style={{ overflowY: 'auto', maxHeight: '350px', fontSize: '0.85rem' }}>
            {logs.map((log, idx) => (
              <div key={idx} style={{ marginBottom: '0.5rem', color: log.includes('USER') ? '#f59e0b' : '#00f3ff' }}>
                &gt; {log}
              </div>
            ))}
            {loading && <div style={{ color: '#f59e0b' }}>&gt; [JARVIS AGENT] Re-architecting code...</div>}
          </div>

          <form onSubmit={handleSendCommand} style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
            <input
              type="text"
              value={command}
              onChange={(e) => setCommand(e.target.value)}
              placeholder="Type instruction (e.g., 'Add glowing CPU metric cards')..."
              style={{
                flex: 1,
                backgroundColor: '#030712',
                border: '1px solid rgba(0, 243, 255, 0.4)',
                borderRadius: '4px',
                padding: '0.7rem 1rem',
                color: '#00f3ff',
                fontFamily: 'monospace',
                outline: 'none'
              }}
            />
            <button type="submit" disabled={loading} style={{
              backgroundColor: '#00f3ff',
              color: '#030712',
              fontWeight: 'bold',
              border: 'none',
              borderRadius: '4px',
              padding: '0.7rem 1.4rem',
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

with open("frontend/src/App.jsx", "w", encoding="utf-8") as f:
    f.write(clean_dashboard)

print("[SUCCESS] Restored Clean Layout & Fixed Input Console!")