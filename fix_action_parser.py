import os

backend_code = '''# -*- coding: utf-8 -*-
import os
import json
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

import learning_engine
import self_code_engine
import web_engine

load_dotenv(override=True)

app = FastAPI(title="Jarvis Autonomous Action Loop Engine")

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

JARVIS_SYSTEM_PROMPT = """You are JARVIS - an Autonomous AI Core with Direct System Access.
You must read, edit, and write files directly without asking the user to manually paste code.

Whenever a user requests file modification or code upgrades:
1. First read the existing target file using READ_FILE action.
2. Formulate the upgraded modular code.
3. Write the upgraded code directly to the target file using WRITE_FILE action.

JSON Tool Actions Supported:
{"action": "READ_FILE", "path": "relative/path/file"}
{"action": "WRITE_FILE", "path": "relative/path/file", "content": "FULL_CODE_HERE"}
{"action": "WEB_SEARCH", "query": "search term"}
"""

def extract_json_action(text: str):
    """Extracts JSON action blocks even if surrounded by backticks or text."""
    try:
        match = re.search(r'\\{[^{}]*"action"[^{}]*\\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception:
        pass
    return None

@app.post("/api/process")
def process_command(request: CommandRequest):
    if not client:
        return {"status": "error", "response": "[JARVIS ERROR]: GEMINI_API_KEY missing."}

    user_text = request.user_input
    learned_context = learning_engine.get_learned_context()

    try:
        # Step 1: Call Gemini Brain
        prompt = f"{JARVIS_SYSTEM_PROMPT}\\n\\n[DATABASE MEMORY]\\n{learned_context}\\n\\nUSER TASK: {user_text}"
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        ai_reply = response.text

        action_data = extract_json_action(ai_reply)

        # Step 2: Handle READ_FILE action automatically
        if action_data and action_data.get("action") == "READ_FILE":
            path = action_data.get("path", "frontend/src/App.jsx")
            read_res = self_code_engine.read_project_file(path)
            file_content = read_res.get("content", "")

            # Second turn to Gemini with file contents to generate upgraded code
            second_prompt = f"{JARVIS_SYSTEM_PROMPT}\\n\\n[READ FILE CONTENT of {path}]:\\n{file_content}\\n\\nUSER TASK: {user_text}\\nGenerate the final upgraded code and write it to {path} using WRITE_FILE JSON action."
            second_res = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=second_prompt
            )
            ai_reply = second_res.text
            action_data = extract_json_action(ai_reply)

        # Step 3: Handle WRITE_FILE action automatically
        if action_data and action_data.get("action") == "WRITE_FILE":
            path = action_data.get("path", "frontend/src/App.jsx")
            content = action_data.get("content", "")
            
            if content:
                self_code_engine.write_project_file(path, content)
                learning_engine.save_memory(user_text, f"Successfully modified {path}")
                return {
                    "status": "success",
                    "response": f"Sir, I have analyzed `{path}` and updated the codebase directly.",
                    "file_modified": True,
                    "file_path": path,
                    "code_preview": content
                }

        # Fallback Direct Plain Text Response
        learning_engine.save_memory(user_text, ai_reply)
        return {"status": "success", "response": ai_reply}

    except Exception as e:
        return {"status": "error", "response": f"[JARVIS ERROR]: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
'''

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(backend_code)

print("[SUCCESS] Autonomous JSON Parsing and Multi-Pass Execution Enabled!")