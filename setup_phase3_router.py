import os

orchestrator_code = '''# -*- coding: utf-8 -*-
import re

def analyze_intent(user_input: str) -> str:
    \"\"\"Analyzes user input and determines the optimal tool/execution path.\"\"\"
    text = user_input.lower()
    
    # Check for Web Scraping / Fetching Intent
    if any(k in text for k in ["http://", "https://", "fetch page", "scrape"]):
        return "WEB_SCRAPE"
        
    # Check for Python Execution / Code Sandbox Intent
    if "def " in text or "import " in text or "print(" in text or "run code" in text:
        return "EXECUTE_CODE"
        
    return "LLM_CHAT"
'''

main_router_code = '''# -*- coding: utf-8 -*-
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv
from google import genai
import learning_engine
import executor
import orchestrator
import web_engine

load_dotenv(override=True)

app = FastAPI(title="Jarvis Autonomous Orchestrator Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini_key = os.getenv("GEMINI_API_KEY", "")
client = genai.Client(api_key=gemini_key) if gemini_key else None

conversation_history: List[Dict[str, str]] = []

JARVIS_SYSTEM_PROMPT = """You are JARVIS - an Autonomous AI Core & Multi-Engine Software Architect.
1. Provide accurate, modular, and direct answers.
2. Utilize learned context from database memories and executed tool outputs seamlessly.
"""

class CommandRequest(BaseModel):
    user_input: str

class ExecuteRequest(BaseModel):
    code: str

class ScrapeRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"status": "Jarvis Orchestrator Active", "database": "Supabase Connected"}

@app.post("/api/process")
def process_command(request: CommandRequest):
    global conversation_history

    if not client:
        return {"status": "error", "response": "[JARVIS ERROR]: GEMINI_API_KEY is missing."}

    try:
        # Step 1: Intent Routing
        intent = orchestrator.analyze_intent(request.user_input)
        extra_context = ""

        # Step 2: Auto Scrape if URL present
        if intent == "WEB_SCRAPE":
            urls = [word for word in request.user_input.split() if word.startswith("http")]
            if urls:
                scrape_res = web_engine.fetch_web_page_content(urls[0])
                if scrape_res.get("status") == "success":
                    extra_context = f"\\n[LIVE WEB CONTENT EXTRACTED FROM {urls[0]}]:\\n{scrape_res.get('content')[:1500]}\\n"

        # Step 3: Fetch Database Learned Memory
        learned_context = learning_engine.get_learned_context()

        # Step 4: Construct Full Context
        prompt_content = f"{JARVIS_SYSTEM_PROMPT}\\n\\n[DATABASE MEMORY]\\n{learned_context}\\n{extra_context}\\n"
        
        conversation_history.append({"role": "user", "content": request.user_input})
        trimmed_history = conversation_history[-6:]
        
        for msg in trimmed_history:
            prompt_content += f"{msg['role'].upper()}: {msg['content']}\\n"

        # Step 5: AI Generation Call
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt_content,
        )

        ai_reply = response.text

        # Step 6: Save conversation to Supabase Cloud Memory
        conversation_history.append({"role": "assistant", "content": ai_reply})
        learning_engine.save_memory(request.user_input, ai_reply)

        return {
            "status": "success",
            "intent_detected": intent,
            "response": ai_reply,
            "memory_saved": True
        }

    except Exception as e:
        return {
            "status": "error",
            "response": f"[JARVIS ERROR]: {str(e)}"
        }

@app.post("/api/execute")
def execute_code(request: ExecuteRequest):
    res = executor.run_python_code(request.code)
    learning_engine.save_memory(f"CODE EXECUTION TEST", str(res))
    return res

@app.post("/api/scrape")
def scrape_url(request: ScrapeRequest):
    return web_engine.fetch_web_page_content(request.url)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
'''

with open("backend/orchestrator.py", "w", encoding="utf-8") as f:
    f.write(orchestrator_code)

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(main_router_code)

print("[SUCCESS] Phase 3: Autonomous Orchestrator and Smart Router active!")