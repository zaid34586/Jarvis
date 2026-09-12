import os

main_code = '''# -*- coding: utf-8 -*-
import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv
from google import genai

import learning_engine
import executor
import web_engine
import self_code_engine

load_dotenv(override=True)

app = FastAPI(title="Jarvis Fast Autonomous Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini_key = os.getenv("GEMINI_API_KEY", "")
client = genai.Client(api_key=gemini_key) if gemini_key else None

class CommandRequest(BaseModel):
    user_input: str

class ExecuteRequest(BaseModel):
    code: str

class ScrapeRequest(BaseModel):
    url: str

JARVIS_SYSTEM_PROMPT = """You are JARVIS - an Advanced Autonomous AI Core.
1. Provide fast, precise, and direct answers.
2. Adapt using context and memory history.
"""

@app.get("/")
def read_root():
    return {"status": "Jarvis Fast Core Online"}

@app.get("/api/process")
def process_get():
    return {"status": "Active", "message": "Use POST method for commands."}

@app.post("/api/process")
def process_command(request: CommandRequest):
    if not client:
        return {"status": "error", "response": "[JARVIS ERROR]: GEMINI_API_KEY is missing."}

    try:
        learned_context = learning_engine.get_learned_context()
        prompt = f"{JARVIS_SYSTEM_PROMPT}\\n\\n[DATABASE MEMORY]\\n{learned_context}\\n\\nUSER TASK: {request.user_input}"

        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        ai_reply = response.text

        # Background async-like save to prevent UI lag
        try:
            learning_engine.save_memory(request.user_input, ai_reply)
        except Exception:
            pass

        return {"status": "success", "response": ai_reply}

    except Exception as e:
        return {"status": "error", "response": f"[JARVIS ERROR]: {str(e)}"}

@app.post("/api/execute")
def execute_code(request: ExecuteRequest):
    res = executor.run_python_code(request.code)
    return res

@app.post("/api/scrape")
def scrape_url(request: ScrapeRequest):
    return web_engine.fetch_web_page_content(request.url)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
'''

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(main_code)

print("[SUCCESS] Optimized Fast Backend main.py deployed!")