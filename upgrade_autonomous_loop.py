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

app = FastAPI(title="Jarvis Autonomous Loop Core")

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

JARVIS_SYSTEM_PROMPT = """You are JARVIS - a Fully Autonomous AI Core capable of Self-Improvement and Web Learning.
You have access to tool actions. Respond in JSON when requesting action execution, or return a standard text reply.

Allowed Actions:
1. WEB_SEARCH: {"action": "WEB_SEARCH", "query": "search text"}
2. READ_FILE: {"action": "READ_FILE", "path": "relative/path/to/file"}
3. WRITE_FILE: {"action": "WRITE_FILE", "path": "relative/path/to/file", "content": "file text"}
4. EXECUTE_CODE: {"action": "EXECUTE_CODE", "code": "python code"}

If no tool action is needed, respond with direct helpful plain text.
"""

@app.get("/")
def read_root():
    return {"status": "Jarvis Autonomous Multi-Step Engine Active"}

@app.post("/api/process")
def process_command(request: CommandRequest):
    if not client:
        return {"status": "error", "response": "[JARVIS ERROR]: GEMINI_API_KEY is missing."}

    learned_context = learning_engine.get_learned_context()
    prompt = f"{JARVIS_SYSTEM_PROMPT}\\n\\n[DATABASE MEMORY]\\n{learned_context}\\n\\nUSER TASK: {request.user_input}"

    try:
        # Loop execution attempt
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        ai_raw = response.text

        # Check for JSON action
        if ai_raw.strip().startswith("{") and "action" in ai_raw:
            try:
                action_data = json.loads(ai_raw.strip())
                action = action_data.get("action")
                tool_output = ""

                if action == "WEB_SEARCH":
                    tool_output = web_engine.live_web_search(action_data.get("query", ""))
                elif action == "READ_FILE":
                    tool_output = json.dumps(self_code_engine.read_project_file(action_data.get("path", "")))
                elif action == "WRITE_FILE":
                    tool_output = json.dumps(self_code_engine.write_project_file(action_data.get("path", ""), action_data.get("content", "")))
                elif action == "EXECUTE_CODE":
                    tool_output = json.dumps(executor.run_python_code(action_data.get("code", "")))

                # Second pass with tool result
                second_prompt = f"{prompt}\\n\\n[ACTION EXECUTED]: {action}\\n[TOOL OUTPUT]: {tool_output}\\nProvide final synthesis:"
                final_res = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=second_prompt
                )
                ai_reply = final_res.text
            except Exception:
                ai_reply = ai_raw
        else:
            ai_reply = ai_raw

        learning_engine.save_memory(request.user_input, ai_reply)
        return {"status": "success", "response": ai_reply}

    except Exception as e:
        return {"status": "error", "response": f"[JARVIS ERROR]: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
'''

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(main_code)

print("[SUCCESS] Autonomous Tool Loop Integrated into main.py!")