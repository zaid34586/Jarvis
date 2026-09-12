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

load_dotenv(override=True)

app = FastAPI(title="Jarvis Clean Code Sanitizer Engine")

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

def sanitize_jsx_code(raw_text: str) -> str:
    """Extracts valid JSX code without JSON wrappers or markdown code blocks."""
    # Check JSON wrapper first
    try:
        match = re.search(r'\\{[^{}]*"action"[^{}]*\\}', raw_text, re.DOTALL)
        if match:
            obj = json.loads(match.group(0))
            if "content" in obj:
                raw_text = obj["content"]
    except Exception:
        pass

    # Strip Markdown ``` blocks if present
    if "```" in raw_text:
        parts = raw_text.split("```")
        for p in parts:
            if "import React" in p or "export default" in p:
                raw_text = p.replace("jsx", "").replace("javascript", "").strip()
                break

    return raw_text.strip()

@app.post("/api/process")
def process_command(request: CommandRequest):
    if not client:
        return {"status": "error", "response": "[JARVIS ERROR]: GEMINI_API_KEY missing."}

    user_text = request.user_input

    try:
        prompt = f"You are JARVIS. Generate valid React JSX code for frontend/src/App.jsx. Do NOT wrap in raw JSON string when outputting code.\\n\\nUSER TASK: {user_text}"
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        ai_reply = response.text
        clean_code = sanitize_jsx_code(ai_reply)

        if "import React" in clean_code or "export default" in clean_code:
            self_code_engine.write_project_file("frontend/src/App.jsx", clean_code)
            return {
                "status": "success",
                "response": "Sir, I have cleaned and updated `frontend/src/App.jsx`.",
                "file_modified": True,
                "file_path": "frontend/src/App.jsx",
                "code_preview": clean_code
            }

        return {"status": "success", "response": ai_reply}

    except Exception as e:
        return {"status": "error", "response": f"[JARVIS ERROR]: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
'''

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(backend_code)

print("[SUCCESS] Applied Clean Code Sanitizer to backend/main.py!")