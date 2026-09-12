import os

gemini_code = '''# -*- coding: utf-8 -*-
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
import prompt_builder

load_dotenv(override=True)

app = FastAPI(title="Jarvis Gemini Autonomous Engine")

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

JARVIS_SYSTEM_PROMPT = """You are JARVIS - an Advanced Autonomous AI Core & Software Architect.
1. Provide concise, modular code and direct answers.
2. Adapt using context and memory history.
"""

class CommandRequest(BaseModel):
    user_input: str

class ExecuteRequest(BaseModel):
    code: str

class ScrapeRequest(BaseModel):
    url: str

class SearchRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"status": "Jarvis Brain Active", "mode": "Google Gemini Free Engine Active"}

@app.post("/api/process")
def process_command(request: CommandRequest):
    global conversation_history

    if not client:
        return {"status": "error", "response": "[JARVIS ERROR]: GEMINI_API_KEY is missing in .env file."}

    try:
        learned_context = learning_engine.get_learned_context()
        prompt_content = f"{JARVIS_SYSTEM_PROMPT}\\n\\n[LEARNED CONTEXT]\\n{learned_context}\\n\\n"
        
        conversation_history.append({"role": "user", "content": request.user_input})
        trimmed_history = conversation_history[-6:]
        
        for msg in trimmed_history:
            prompt_content += f"{msg['role'].upper()}: {msg['content']}\\n"

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_content,
        )

        ai_reply = response.text

        conversation_history.append({"role": "assistant", "content": ai_reply})
        learning_engine.save_memory(request.user_input, ai_reply)

        return {
            "status": "success",
            "input": request.user_input,
            "response": ai_reply,
            "learned_entries": len(learning_engine.load_memory())
        }

    except Exception as e:
        return {
            "status": "error",
            "input": request.user_input,
            "response": f"[JARVIS ERROR]: {str(e)}"
        }

@app.post("/api/execute")
def execute_code(request: ExecuteRequest):
    res = executor.run_python_code(request.code)
    learning_engine.save_memory(f"EXECUTED CODE: {request.code[:50]}...", str(res))
    return res

@app.post("/api/scrape")
def scrape_url(request: ScrapeRequest):
    data = web_engine.fetch_web_page_content(request.url)
    if data["status"] == "success":
        learning_engine.save_memory(f"WEB SCRAPE: {request.url}", data["content"][:200])
    return data

@app.post("/api/web-search")
def web_search(request: SearchRequest):
    return web_engine.mock_web_search(request.query)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
'''

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(gemini_code)

print("[SUCCESS] Switched backend to Gemini!")