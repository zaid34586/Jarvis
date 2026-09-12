import os

hub_code = '''import React, { useState, useEffect } from "react";
import { Terminal, Cpu, Shield, Activity, Database, FileCode, Mic, Send, RefreshCw } from "lucide-react";

export default function App() {
  const [activeTab, setActiveTab] = useState("diff");
  const [inputPrompt, setInputPrompt] = useState("");
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Jarvis Autonomous Core online. How can I assist you today?" }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [memories, setMemories] = useState([]);
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
    <div className="flex h-screen bg-[#07090e] text-slate-200 font-mono selection:bg-emerald-500 selection:text-black overflow-hidden">
      {/* Left Panel: Chat & Control Console */}
      <div className="w-1/2 flex flex-col border-r border-slate-800 bg-slate-950/60">
        <header className="border-b border-slate-800/80 px-6 py-4 flex items-center justify-between bg-slate-950">
          <div className="flex items-center gap-3">
            <div className="flex space-x-1.5">
              <div className="w-3 h-3 rounded-full bg-rose-500/80" />
              <div className="w-3 h-3 rounded-full bg-amber-500/80" />
              <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
            </div>
            <span className="text-slate-700">|</span>
            <div className="flex items-center gap-2 text-xs font-bold text-emerald-400">
              <Terminal className="w-4 h-4" />
              <span>JARVIS // AUTONOMOUS_CORE</span>
            </div>
          </div>
          <span className="text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1 rounded-full">
            SYSTEM ONLINE
          </span>
        </header>

        {/* Chat Feed */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, idx) => (
            <div key={idx} className={`p-4 rounded-xl text-xs leading-relaxed border ${
              msg.role === "user" 
                ? "bg-slate-900/90 border-slate-700/60 text-slate-100 ml-8" 
                : "bg-slate-950 border-emerald-500/30 text-emerald-300 mr-8"
            }`}>
              <div className="text-[10px] text-slate-500 mb-1">
                [{msg.role === "user" ? "USER" : "JARVIS_BRAIN"}]
              </div>
              <pre className="whitespace-pre-wrap font-mono">{msg.content}</pre>
            </div>
          ))}
          {isLoading && (
            <div className="flex items-center gap-2 text-xs text-emerald-400 animate-pulse">
              <RefreshCw className="w-4 h-4 animate-spin" /> Processing Autonomous Action Loop...
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/80">
          <div className="flex gap-2">
            <button className="p-3 bg-slate-900 border border-slate-800 rounded-lg text-slate-400 hover:text-emerald-400 transition-colors">
              <Mic className="w-4 h-4" />
            </button>
            <input
              type="text"
              value={inputPrompt}
              onChange={(e) => setInputPrompt(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Type command or instruct self-code modification..."
              className="flex-1 bg-slate-900/90 border border-slate-800 rounded-lg px-4 text-xs text-slate-100 focus:outline-none focus:border-emerald-500/50"
            />
            <button 
              onClick={handleSend}
              className="px-4 py-3 bg-emerald-500 hover:bg-emerald-400 text-black font-bold rounded-lg transition-colors flex items-center justify-center">
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Right Panel: Live Code Diff & Database Telemetry */}
      <div className="w-1/2 flex flex-col bg-[#05070b]">
        <div className="flex border-b border-slate-800 bg-slate-950">
          <button
            onClick={() => setActiveTab("diff")}
            className={`px-6 py-3 text-xs font-bold border-r border-slate-800 flex items-center gap-2 transition-colors ${
              activeTab === "diff" ? "bg-slate-900 text-emerald-400 border-b-2 border-b-emerald-500" : "text-slate-500"
            }`}>
            <FileCode className="w-4 h-4" /> Code Inspector & Diff
          </button>
          <button
            onClick={() => setActiveTab("memory")}
            className={`px-6 py-3 text-xs font-bold border-r border-slate-800 flex items-center gap-2 transition-colors ${
              activeTab === "memory" ? "bg-slate-900 text-emerald-400 border-b-2 border-b-emerald-500" : "text-slate-500"
            }`}>
            <Database className="w-4 h-4" /> Supabase Memory DB
          </button>
        </div>

        <div className="flex-1 p-6 overflow-auto">
          {activeTab === "diff" ? (
            <div className="h-full rounded-xl border border-slate-800 bg-slate-950 p-4 font-mono text-xs text-slate-300 overflow-auto">
              <pre>{codeDiff}</pre>
            </div>
          ) : (
            <div className="h-full rounded-xl border border-slate-800 bg-slate-950 p-4 font-mono text-xs text-slate-400">
              <p className="text-slate-500 mb-4">// Supabase Cloud Memory Synced Table</p>
              <div className="space-y-2">
                <div className="p-2 border border-slate-800 rounded bg-slate-900/50 text-emerald-400">
                  Memory Sync: Active (Supabase PostgreSQL)
                </div>
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
    f.write(hub_code)

print("[SUCCESS] Frontend upgraded to dual-panel Autonomous Control Hub!")