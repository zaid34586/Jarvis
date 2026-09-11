# -*- coding: utf-8 -*-
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
import learning_engine
import executor

load_dotenv()

app = FastAPI(title="Jarvis Autonomous Engine V3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key"))

conversation_history: List[Dict[str, str]] = []

JARVIS_BUSINESS_SYSTEM_PROMPT = """You are JARVIS - an Autonomous AI Core and System Execution Architect.
Primary Directive:
1. Provide optimized code or execution strategies.
2. Evaluate business logic, scalability, and execution stability.
3. Learn from past interactions to optimize future workflows.
"""

class CommandRequest(BaseModel):
    user_input: str

class ExecuteRequest(BaseModel):
    code: str

@app.get("/")
def read_root():
    return {"status": "Jarvis Brain Active", "mode": "Execution Engine & Sandbox Ready"}

@app.post("/api/process")
def process_command(request: CommandRequest):
    global conversation_history

    try:
        learned_context = learning_engine.get_learned_context()
        
        system_message = {
            "role": "system", 
            "content": f"{JARVIS_BUSINESS_SYSTEM_PROMPT}\n\n[LEARNED CONTEXT]\n{learned_context}"
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
    """Executes code directly in Python sandbox and logs result to memory."""
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
