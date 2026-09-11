import os

env_content = """OPENAI_API_KEY=your_openai_api_key_here
"""

requirements_content = """fastapi
uvicorn
pydantic
python-dotenv
openai
requests
"""

learning_store_content = '''# -*- coding: utf-8 -*-
import json
import os
from typing import List, Dict

LEARNING_FILE = "jarvis_memory.json"

def load_memory() -> List[Dict]:
    if not os.path.exists(LEARNING_FILE):
        return []
    try:
        with open(LEARNING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_memory(user_prompt: str, ai_response: str, feedback: str = "success"):
    memory = load_memory()
    entry = {
        "user_prompt": user_prompt,
        "ai_response": ai_response,
        "feedback": feedback
    }
    memory.append(entry)
    with open(LEARNING_FILE, "w", encoding="utf-8") as f:
        json.dump(memory[-50:], f, indent=2, ensure_ascii=False)

def get_learned_context() -> str:
    memory = load_memory()
    if not memory:
        return "No past learning context available."
    
    summary = "Past successful interactions and patterns:\\n"
    for item in memory[-5:]:
        clean_resp = item['ai_response'][:100].replace("\\n", " ")
        summary += f"- User requested: {item['user_prompt']} | Strategy used: {clean_resp}...\\n"
    return summary
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

load_dotenv()

app = FastAPI(title="Jarvis Autonomous Brain V2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key"))

conversation_history: List[Dict[str, str]] = []

JARVIS_BUSINESS_SYSTEM_PROMPT = """You are JARVIS - an Autonomous, Business-Minded AI Core and Software Architect.
Your Primary Directive:
1. Always evaluate tasks with a Strategic & Business Mindset (efficiency, scalability, ROI, low execution risk).
2. Provide direct, highly structured, production-ready code or operational steps.
3. Learn from past interactions and adapt to the user's workflow style.
4. If a task requires code execution or automation, prepare structured execution plans.
"""

class CommandRequest(BaseModel):
    user_input: str

@app.get("/")
def read_root():
    return {"status": "Jarvis Brain Active", "mode": "Business & Learning Engine Enabled"}

@app.post("/api/process")
def process_command(request: CommandRequest):
    global conversation_history

    try:
        learned_context = learning_engine.get_learned_context()
        
        system_message = {
            "role": "system", 
            "content": f"{JARVIS_BUSINESS_SYSTEM_PROMPT}\\n\\n[MINI-LEARNING MEMORY CONTEXT]\\n{learned_context}"
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
        fallback_msg = f"[JARVIS BRAIN OFFLINE / CONFIG ERROR]: {str(e)}"
        return {
            "status": "error",
            "input": request.user_input,
            "response": fallback_msg,
            "learned_entries": 0
        }

@app.post("/api/clear-memory")
def clear_memory():
    global conversation_history
    conversation_history = []
    return {"status": "Short-term conversation memory cleared."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
'''

os.makedirs("backend", exist_ok=True)

with open("backend/.env", "w", encoding="utf-8") as f:
    f.write(env_content)

with open("backend/requirements.txt", "w", encoding="utf-8") as f:
    f.write(requirements_content)

with open("backend/learning_engine.py", "w", encoding="utf-8") as f:
    f.write(learning_store_content)

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(main_py_content)

print("[SUCCESS] All files written cleanly with correct formatting and syntax!")