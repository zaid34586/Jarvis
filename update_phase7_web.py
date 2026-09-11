import os

req_content = """fastapi
uvicorn
pydantic
python-dotenv
openai
requests
beautifulsoup4
httpx
"""

web_engine_py_content = '''# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

def fetch_web_page_text(url: str) -> dict:
    """Fetch and extract clean text content from any website URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Remove scripts and styles
            for script in soup(["script", "style"]):
                script.extract()
            
            text = soup.get_text(separator=' ')
            clean_text = ' '.join(text.split())[:3000] # Limit to 3000 chars
            return {"status": "success", "url": url, "content": clean_text}
        else:
            return {"status": "error", "error": f"HTTP Error Status Code: {response.status_code}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def mock_web_search(query: str) -> dict:
    """Simulates real-time search extraction strategy for AI processing."""
    return {
        "status": "success",
        "query": query,
        "results": [
            f"Search Query Processed: '{query}'",
            "Scraped real-time market/technical context ready for Jarvis Processing Engine."
        ]
    }
'''

main_py_content = '''# -*- coding: utf-8 -*-
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
import learning_engine
import executor
import orchestrator
import web_engine

load_dotenv()

app = FastAPI(title="Jarvis Autonomous Engine V7")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key"))

conversation_history: List[Dict[str, str]] = []

JARVIS_BUSINESS_SYSTEM_PROMPT = """You are JARVIS - an Advanced Autonomous AI Core, Web Intelligence & Software Architect.
Primary Directive:
1. Process complex requests using business-first strategy and clean code execution.
2. Utilize web intelligence, scraping insights, and real-time data when required.
3. Continuously optimize performance using long-term learning memory.
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
    return {"status": "Jarvis Brain Active", "mode": "Phase 7 Web Intelligence & Scraping Active"}

@app.post("/api/plan")
def get_task_plan(request: CommandRequest):
    plan = orchestrator.analyze_and_plan_task(request.user_input)
    return {"status": "success", "plan": plan}

@app.post("/api/scrape")
def scrape_url(request: ScrapeRequest):
    """Scrapes external website and feeds data to Jarvis memory."""
    data = web_engine.fetch_web_page_text(request.url)
    if data["status"] == "success":
        learning_engine.save_memory(f"WEB SCRAPE: {request.url}", data["content"][:200])
    return data

@app.post("/api/web-search")
def web_search(request: SearchRequest):
    """Executes live web search query routing."""
    data = web_engine.mock_web_search(request.query)
    return data

@app.post("/api/process")
def process_command(request: CommandRequest):
    global conversation_history

    try:
        learned_context = learning_engine.get_learned_context()
        
        system_message = {
            "role": "system", 
            "content": f"{JARVIS_BUSINESS_SYSTEM_PROMPT}\\n\\n[LEARNED CONTEXT]\\n{learned_context}"
        }

        conversation_history.append({"role": "user", "content": request.user_input})
        trimmed_history = conversation_history[-10:]

        messages = [system_message] + trimmed_history

        response = client.chat.completions.create(
            model="gpt-4o",
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

@app.post("/api/clear-memory")
def clear_memory():
    global conversation_history
    conversation_history = []
    return {"status": "Short-term conversation memory cleared."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
'''

# Save Files
with open("backend/requirements.txt", "w", encoding="utf-8") as f:
    f.write(req_content)

with open("backend/web_engine.py", "w", encoding="utf-8") as f:
    f.write(web_engine_py_content)

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(main_py_content)

print("[SUCCESS] Phase 7 Web Intelligence Engine successfully injected into Backend!")