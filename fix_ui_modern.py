import os

inline_ui_code = '''import React, { useState, useEffect } from "react";

export default function App() {
  const [activeTab, setActiveTab] = useState("diff");
  const [inputPrompt, setInputPrompt] = useState("");
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Jarvis Autonomous Core online. Systems operational." }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [codeDiff, setCodeDiff] = useState("// Waiting for autonomous file modifications...");

  const handleSend = async () => {
    if (!inputPrompt.trim()) return;
    
    const userMsg = inputPrompt;
    setInputPrompt("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setIsLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: userMsg }),
      });
      const data = await res.json();
      
      const reply = data.response || "[SYSTEM ERROR]: No response generated.";
      setMessages((prev) => [...prev, { role: "assistant", content: reply }]);

      if (data.file_modified) {
        setCodeDiff(`// Modified File: ${data.file_path || "App.jsx"}\\n\\n${data.code_preview || ""}`);
      }
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: "[SYSTEM ERROR]: Backend unreachable." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{
      display: 'flex',
      height: '100vh',
      backgroundColor: '#07090e',
      color: '#e2e8f0',
      fontFamily: 'monospace',
      overflow: 'hidden'
    }}>
      {/* Left Panel: Chat & Control Console */}
      <div style={{
        width: '50%',
        display: 'flex',
        flexDirection: 'column',
        borderRight: '1px solid #1e293b',
        backgroundColor: '#0a0d14'
      }}>
        {/* Header */}
        <div style={{
          padding: '16px 24px',
          borderBottom: '1px solid #1e293b',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          backgroundColor: '#06080d'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ color: '#10b981', fontWeight: 'bold', fontSize: '14px' }}>&gt;_ JARVIS // AUTONOMOUS_CORE</span>
          </div>
          <span style={{
            fontSize: '11px',
            color: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            border: '1px solid rgba(16, 185, 129, 0.2)',
            padding: '4px 10px',
            borderRadius: '12px'
          }}>
            SYSTEM ONLINE
          </span>
        </div>

        {/* Chat Feed */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '24px',
          display: 'flex',
          flexDirection: 'column',
          gap: '16px'
        }}>
          {messages.map((msg, idx) => (
            <div key={idx} style={{
              padding: '12px 16px',
              borderRadius: '8px',
              fontSize: '12px',
              lineHeight: '1.6',
              border: msg.role === 'user' ? '1px solid #334155' : '1px solid rgba(16, 185, 129, 0.3)',
              backgroundColor: msg.role === 'user' ? '#0f172a' : '#040d12',
              color: msg.role === 'user' ? '#f8fafc' : '#34d399',
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              maxWidth: '85%'
            }}>
              <div style={{ fontSize: '10px', color: '#64748b', marginBottom: '4px' }}>
                [{msg.role === 'user' ? 'USER' : 'JARVIS_BRAIN'}]
              </div>
              <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
            </div>
          ))}
          {isLoading && (
            <div style={{ fontSize: '12px', color: '#34d399' }}>
              &gt; Processing Autonomous Action Loop...
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div style={{
          padding: '16px',
          borderTop: '1px solid #1e293b',
          backgroundColor: '#06080d',
          display: 'flex',
          gap: '8px'
        }}>
          <input
            type="text"
            value={inputPrompt}
            onChange={(e) => setInputPrompt(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type command or instruct self-code modification..."
            style={{
              flex: 1,
              backgroundColor: '#0f172a',
              border: '1px solid #1e293b',
              borderRadius: '6px',
              padding: '10px 14px',
              color: '#f8fafc',
              fontSize: '12px',
              fontFamily: 'monospace',
              outline: 'none'
            }}
          />
          <button
            onClick={handleSend}
            style={{
              backgroundColor: '#10b981',
              color: '#000',
              fontWeight: 'bold',
              border: 'none',
              borderRadius: '6px',
              padding: '10px 20px',
              cursor: 'pointer',
              fontSize: '12px'
            }}>
            SEND
          </button>
        </div>
      </div>

      {/* Right Panel: Code Inspector & Database Logs */}
      <div style={{
        width: '50%',
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: '#05070b'
      }}>
        <div style={{ display: 'flex', borderBottom: '1px solid #1e293b', backgroundColor: '#06080d' }}>
          <button
            onClick={() => setActiveTab("diff")}
            style={{
              padding: '12px 20px',
              fontSize: '12px',
              fontWeight: 'bold',
              border: 'none',
              borderRight: '1px solid #1e293b',
              backgroundColor: activeTab === 'diff' ? '#0f172a' : 'transparent',
              color: activeTab === 'diff' ? '#34d399' : '#64748b',
              cursor: 'pointer'
            }}>
            Code Inspector & Diff
          </button>
          <button
            onClick={() => setActiveTab("memory")}
            style={{
              padding: '12px 20px',
              fontSize: '12px',
              fontWeight: 'bold',
              border: 'none',
              borderRight: '1px solid #1e293b',
              backgroundColor: activeTab === 'memory' ? '#0f172a' : 'transparent',
              color: activeTab === 'memory' ? '#34d399' : '#64748b',
              cursor: 'pointer'
            }}>
            Supabase Memory DB
          </button>
        </div>

        <div style={{ flex: 1, padding: '20px', overflow: 'auto' }}>
          {activeTab === 'diff' ? (
            <div style={{
              height: '100%',
              borderRadius: '8px',
              border: '1px solid #1e293b',
              backgroundColor: '#040d12',
              padding: '16px',
              fontSize: '12px',
              color: '#94a3b8',
              overflow: 'auto'
            }}>
              <pre style={{ margin: 0 }}>{codeDiff}</pre>
            </div>
          ) : (
            <div style={{
              height: '100%',
              borderRadius: '8px',
              border: '1px solid #1e293b',
              backgroundColor: '#040d12',
              padding: '16px',
              fontSize: '12px',
              color: '#64748b'
            }}>
              <p style={{ color: '#34d399', margin: '0 0 10px 0' }}>// Supabase Cloud Memory Synced Table</p>
              <div style={{ padding: '10px', border: '1px solid #1e293b', borderRadius: '4px', backgroundColor: '#0a0d14' }}>
                Memory Sync: Active (Supabase PostgreSQL)
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
'''

with open("frontend/src/App.jsx", "w", encoding="utf-8") as f:
    f.write(inline_ui_code)

print("[SUCCESS] Applied Bulletproof Inline Styled Dark Terminal Dashboard!")