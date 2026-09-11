import os

prompt_builder_py_content = '''# -*- coding: utf-8 -*-

def build_custom_prompt(task_type: str, user_requirement: str) -> str:
    """Generates highly structured, targeted system prompts for sub-tasks."""
    base_prompt = f"""[SYSTEM ROLE: SPECIALIZED {task_type.upper()} AGENT]
CONTEXT & GOAL:
{user_requirement}

EXECUTION RULES:
1. Provide production-ready, highly efficient, modular code or operational steps.
2. Include error handling, safety checks, and edge-case validations.
3. Keep explanation concise, structured, and focused on immediate deployment.

OUTPUT FORMAT:
- Executive Summary (1-2 lines)
- Structured Code / Configuration
- Terminal / Execution Commands
"""
    return base_prompt
'''

cli_controller_content = '''# -*- coding: utf-8 -*-
import requests
import sys

API_URL = "http://127.0.0.1:8000"

def run_cli():
    print("==========================================")
    print("   JARVIS AUTONOMOUS CLI CONTROLLER       ")
    print("==========================================")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("Jarvis-CLI > ")
            if user_input.lower() in ["exit", "quit"]:
                break
            if not user_input.trim():
                continue
            
            res = requests.post(f"{API_URL}/api/process", json={"user_input": user_input})
            if res.status_code == 200:
                data = res.json()
                print(f"\n[JARVIS]:\n{data.get('response', '')}\n")
            else:
                print(f"[ERROR]: Status code {res.status_code}")
        except Exception as e:
            print(f"[ERROR]: Connection failed ({str(e)})")

if __name__ == "__main__":
    run_cli()
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
import prompt_builder

load_dotenv()

app = FastAPI(title="Jarvis Complete Autonomous Engine V8")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key"))

conversation_history: List[Dict[str, str]] = []

JARVIS_BUSINESS_SYSTEM_PROMPT = """You are JARVIS - an Advanced Autonomous AI Core, Software Architect & Prompt Engineer.
Primary Directive:
1. Process complex requests using business-first strategy and clean code execution.
2. Utilize web intelligence, scraping insights, and real-time data when required.
3. Automatically generate optimized prompts and automation routines for downstream tasks.
4. Continuously learn and adapt using memory history.
"""

class CommandRequest(BaseModel):
    user_input: str

class ExecuteRequest(BaseModel):
    code: str

class ScrapeRequest(BaseModel):
    url: str

class SearchRequest(BaseModel):
    query: str

class PromptBuildRequest(BaseModel):
    task_type: str
    requirement: str

@app.get("/")
def read_root():
    return {"status": "Jarvis Brain Active", "mode": "Phase 8 Dynamic Prompt Engine & CLI Ready"}

@app.post("/api/plan")
def get_task_plan(request: CommandRequest):
    plan = orchestrator.analyze_and_plan_task(request.user_input)
    return {"status": "success", "plan": plan}

@app.post("/api/generate-prompt")
def generate_prompt(request: PromptBuildRequest):
    """Generates optimized system prompts on demand."""
    generated_prompt = prompt_builder.build_custom_prompt(request.task_type, request.requirement)
    return {"status": "success", "prompt": generated_prompt}

@app.post("/api/scrape")
def scrape_url(request: ScrapeRequest):
    data = web_engine.fetch_web_page_text(request.url)
    if data["status"] == "success":
        learning_engine.save_memory(f"WEB SCRAPE: {request.url}", data["content"][:200])
    return data

@app.post("/api/web-search")
def web_search(request: SearchRequest):
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

with open("backend/prompt_builder.py", "w", encoding="utf-8") as f:
    f.write(prompt_builder_py_content)

with open("jarvis_cli.py", "w", encoding="utf-8") as f:
    f.write(cli_controller_content)

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(main_py_content)

print("[SUCCESS] Phase 8 Dynamic Prompt Builder & CLI Controller generated successfully!")