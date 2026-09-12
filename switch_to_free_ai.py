import os

main_py_groq = '''# -*- coding: utf-8 -*-
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv
from groq import Groq
import learning_engine
import executor
import orchestrator
import web_engine
import prompt_builder

load_dotenv(override=True)

app = FastAPI(title="Jarvis Free Autonomous Engine (Groq Powered)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq Client
groq_api_key = os.getenv("GROQ_API_KEY", "")
client = Groq(api_key=groq_api_key) if groq_api_key else None

conversation_history: List[Dict[str, str]] = []

JARVIS_SYSTEM_PROMPT = """You are JARVIS - an Advanced Free Autonomous AI Core & Software Architect.
Primary Directive:
1. Provide highly accurate, modular code and immediate solutions.
2. Utilize web intelligence, scraping insights, and real-time context.
3. Learn and adapt using memory history.
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
    return {"status": "Jarvis Brain Active", "mode": "Free Groq Llama-3 Engine Active"}

@app.post("/api/process")
def process_command(request: CommandRequest):
    global conversation_history

    if not client:
        return {"status": "error", "response": "[JARVIS ERROR]: GROQ_API_KEY is missing in .env file."}

    try:
        learned_context = learning_engine.get_learned_context()
        
        system_message = {
            "role": "system", 
            "content": f"{JARVIS_SYSTEM_PROMPT}\\n\\n[LEARNED CONTEXT]\\n{learned_context}"
        }

        conversation_history.append({"role": "user", "content": request.user_input})
        trimmed_history = conversation_history[-10:]

        messages = [system_message] + trimmed_history

        # Free Groq High-Speed Llama-3 Model Call
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7
        )

        ai_reply = response.choices[0].message.content

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
    f.write(main_py_groq)

print("[SUCCESS] Backend successfully converted to Free Groq Llama-3 Engine!")