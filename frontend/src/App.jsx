import React, { useState } from 'react';

export default function App() {
  const [input, setInput] = useState('');
  const [code, setCode] = useState("print('Jarvis Autonomous Execution Test')");
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('chat'); // 'chat' or 'executor'

  const handleSendPrompt = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'User', text: input };
    setLogs((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_input: input }),
      });
      const data = await res.json();
      setLogs((prev) => [...prev, { sender: 'Jarvis Brain', text: data.response }]);
    } catch (err) {
      setLogs((prev) => [...prev, { sender: 'System Error', text: 'Backend unreachable.' }]);
    } finally {
      setLoading(false);
      setInput('');
    }
  };

  const handleExecuteCode = async () => {
    if (!code.trim()) return;

    setLogs((prev) => [...prev, { sender: 'System', text: `Executing Sandboxed Code...` }]);
    setLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code }),
      });
      const data = await res.json();
      
      if (data.status === 'success') {
        setLogs((prev) => [...prev, { sender: 'Execution Output', text: data.output }]);
      } else {
        setLogs((prev) => [...prev, { sender: 'Execution Error', text: data.error }]);
      }
    } catch (err) {
      setLogs((prev) => [...prev, { sender: 'System Error', text: 'Execution endpoint failed.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '1.5rem', fontFamily: 'Courier New, monospace', backgroundColor: '#090d16', color: '#00ffcc', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid #00ffcc', paddingBottom: '0.5rem' }}>
        <h2>JARVIS // CONTROL & EXECUTION HUB</h2>
        <div>
          <button onClick={() => setActiveTab('chat')} style={{ padding: '0.5rem 1rem', background: activeTab === 'chat' ? '#00ffcc' : '#1e293b', color: activeTab === 'chat' ? '#000' : '#fff', border: 'none', borderRadius: '4px', marginRight: '0.5rem', cursor: 'pointer', fontWeight: 'bold' }}>
            Brain Prompt
          </button>
          <button onClick={() => setActiveTab('executor')} style={{ padding: '0.5rem 1rem', background: activeTab === 'executor' ? '#00ffcc' : '#1e293b', color: activeTab === 'executor' ? '#000' : '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>
            Code Executor Sandbox
          </button>
        </div>
      </div>

      {activeTab === 'chat' ? (
        <div>
          <div style={{ border: '1px solid #00ffcc', borderRadius: '8px', padding: '1rem', minHeight: '400px', maxHeight: '500px', overflowY: 'auto', marginBottom: '1rem', background: '#030712' }}>
            {logs.map((log, index) => (
              <div key={index} style={{ marginBottom: '1rem', whiteSpace: 'pre-wrap' }}>
                <strong style={{ color: log.sender.includes('Jarvis') ? '#38bdf8' : log.sender === 'User' ? '#a855f7' : '#eab308' }}>
                  [{log.sender}]:
                </strong>
                <p style={{ margin: '0.2rem 0 0 0', color: '#e2e8f0' }}>{log.text}</p>
              </div>
            ))}
            {loading && <div style={{ color: '#eab308' }}>Processing request...</div>}
          </div>

          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendPrompt()}
              placeholder="Type prompt or business task..."
              style={{ flex: 1, padding: '0.75rem', borderRadius: '4px', border: '1px solid #00ffcc', background: '#0f172a', color: '#fff' }}
            />
            <button onClick={handleSendPrompt} style={{ padding: '0.75rem 1.5rem', borderRadius: '4px', background: '#0284c7', color: '#fff', border: 'none', cursor: 'pointer', fontWeight: 'bold' }}>
              SEND
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Python Code Execution Sandbox:</label>
            <textarea
              rows={10}
              value={code}
              onChange={(e) => setCode(e.target.value)}
              style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid #00ffcc', background: '#0f172a', color: '#38bdf8', fontFamily: 'Courier New', fontSize: '14px' }}
            />
          </div>
          <button onClick={handleExecuteCode} style={{ padding: '0.75rem 1.5rem', borderRadius: '4px', background: '#16a34a', color: '#fff', border: 'none', cursor: 'pointer', fontWeight: 'bold', marginBottom: '1rem' }}>
            RUN PYTHON CODE
          </button>

          <div style={{ border: '1px solid #334155', borderRadius: '8px', padding: '1rem', minHeight: '200px', background: '#030712' }}>
            <h4>Execution Logs & Console Output:</h4>
            {logs.map((log, index) => (
              <div key={index} style={{ marginBottom: '0.5rem', color: log.sender.includes('Error') ? '#ef4444' : '#10b981' }}>
                <strong>[{log.sender}]:</strong> <pre style={{ margin: 0 }}>{log.text}</pre>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
