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

app = FastAPI(title="Jarvis Autonomous Engine - Strict React Target")

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

JARVIS_SYSTEM_PROMPT = """You are JARVIS - an Autonomous AI Core.
Target File Constraint:
All UI upgrades or visual changes MUST be written directly to `frontend/src/App.jsx` as valid React JSX code. Do NOT generate standalone HTML (`index.html`).

When user requests UI updates:
1. Return JSX React code for `frontend/src/App.jsx`.
2. Output action JSON format strictly:
{"action": "WRITE_FILE", "path": "frontend/src/App.jsx", "content": "<FULL_JSX_CODE>"}
"""

def extract_json_action(text: str):
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
        prompt = f"{JARVIS_SYSTEM_PROMPT}\\n\\n[MEMORY CONTEXT]\\n{learned_context}\\n\\nUSER TASK: {user_text}"
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        ai_reply = response.text
        action_data = extract_json_action(ai_reply)

        # Force Target Path to frontend/src/App.jsx for any UI action
        if action_data or ("export default" in ai_reply or "import React" in ai_reply):
            target_path = "frontend/src/App.jsx"
            content_to_write = ""

            if action_data and action_data.get("content"):
                content_to_write = action_data.get("content")
            else:
                # Extract JSX from markdown code blocks if present
                if "```" in ai_reply:
                    parts = ai_reply.split("```")
                    for p in parts:
                        if "export default" in p or "import React" in p:
                            content_to_write = p.replace("jsx", "").replace("javascript", "").strip()
                            break
                elif "export default" in ai_reply:
                    content_to_write = ai_reply

            if content_to_write:
                self_code_engine.write_project_file(target_path, content_to_write)
                learning_engine.save_memory(user_text, f"Updated {target_path} successfully.")
                
                return {
                    "status": "success",
                    "response": f"Sir, I have re-architected `frontend/src/App.jsx` with the requested UI upgrade.",
                    "file_modified": True,
                    "file_path": target_path,
                    "code_preview": content_to_write
                }

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

print("[SUCCESS] Applied Strict Target Routing to frontend/src/App.jsx!")