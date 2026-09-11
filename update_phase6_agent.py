import os

orchestrator_py_content = '''# -*- coding: utf-8 -*-
import json

def analyze_and_plan_task(user_prompt: str) -> dict:
    """Break complex user prompts into executable sub-tasks with business priorities."""
    plan = {
        "user_goal": user_prompt,
        "execution_steps": [
            {"step": 1, "action": "Understand Requirement & Plan", "status": "Ready"},
            {"step": 2, "action": "Generate Code/Script", "status": "Pending"},
            {"step": 3, "action": "Execute in Sandboxed Environment", "status": "Pending"},
            {"step": 4, "action": "Verify Output & Log Memory", "status": "Pending"}
        ],
        "business_priority": "High Efficiency / Zero Error Execution"
    }
    return plan
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

load_dotenv()

app = FastAPI(title="Jarvis Multi-Agent Autonomous Engine V6")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key"))

conversation_history: List[Dict[str, str]] = []

JARVIS_BUSINESS_SYSTEM_PROMPT = """You are JARVIS - an Advanced Autonomous AI Agent & Software Architect.
Primary Directive:
1. Deconstruct user tasks into modular executable steps.
2. Optimize execution with strict business efficiency and code accuracy.
3. Automatically leverage past learning context to solve recurring issues.
"""

class CommandRequest(BaseModel):
    user_input: str

class ExecuteRequest(BaseModel):
    code: str

@app.get("/")
def read_root():
    return {"status": "Jarvis Brain Active", "mode": "Phase 6 Multi-Agent Orchestrator Online"}

@app.post("/api/plan")
def get_task_plan(request: CommandRequest):
    """Generates structured execution plan before executing complex tasks."""
    plan = orchestrator.analyze_and_plan_task(request.user_input)
    return {"status": "success", "plan": plan}

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

with open("backend/orchestrator.py", "w", encoding="utf-8") as f:
    f.write(orchestrator_py_content)

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(main_py_content)

print("[SUCCESS] Phase 6 Multi-Agent Orchestrator code successfully injected into Backend!")