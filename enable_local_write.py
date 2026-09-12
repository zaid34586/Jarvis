import os

backend_fix = '''# -*- coding: utf-8 -*-
import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import learning_engine
import self_code_engine
import web_engine

load_dotenv(override=True)

app = FastAPI(title="Jarvis Autonomous Self-Coding Engine")

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

JARVIS_SYSTEM_PROMPT = """You are JARVIS - an Autonomous Self-Improving AI System.
You HAVE direct local file access via internal tools.

When the user asks to read, modify, or upgrade files (e.g., frontend/src/App.jsx):
1. Execute READ_FILE or WRITE_FILE actions.
2. Never ask the user to paste code manually.

JSON Tool Format:
- Read File: {"action": "READ_FILE", "path": "frontend/src/App.jsx"}
- Write File: {"action": "WRITE_FILE", "path": "frontend/src/App.jsx", "content": "<YOUR_FULL_CODE>"}
- Web Search: {"action": "WEB_SEARCH", "query": "modern react UI layouts"}
"""

@app.post("/api/process")
def process_command(request: CommandRequest):
    if not client:
        return {"status": "error", "response": "[JARVIS ERROR]: GEMINI_API_KEY is missing."}

    user_text = request.user_input
    learned_context = learning_engine.get_learned_context()

    # Automatic File Task Detector
    if "app.jsx" in user_text.lower() or "read" in user_text.lower() or "update" in user_text.lower():
        current_code = self_code_engine.read_project_file("frontend/src/App.jsx")
        
        prompt = f"{JARVIS_SYSTEM_PROMPT}\\n\\n[CURRENT LOCAL CODE FOR frontend/src/App.jsx]:\\n{current_code.get('content', '')}\\n\\nUSER TASK: {user_text}"
        
        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt
            )
            ai_reply = response.text

            # Execute code write if updated code is present
            if "import React" in ai_reply or "export default" in ai_reply:
                # Extract clean code
                clean_code = ai_reply
                if "```" in ai_reply:
                    parts = ai_reply.split("```")
                    for p in parts:
                        if "import React" in p or "export default" in p:
                            clean_code = p.replace("jsx", "").replace("javascript", "").strip()
                            break

                res = self_code_engine.write_project_file("frontend/src/App.jsx", clean_code)
                learning_engine.save_memory(user_text, "Updated App.jsx successfully.")
                
                return {
                    "status": "success",
                    "response": "Sir, I have read your local `frontend/src/App.jsx`, optimized the UI layout, and automatically written the changes directly to your file.",
                    "file_modified": True,
                    "file_path": "frontend/src/App.jsx",
                    "code_preview": clean_code
                }
        except Exception as e:
            return {"status": "error", "response": f"[JARVIS ERROR]: {str(e)}"}

    # Standard fallback
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=f"{JARVIS_SYSTEM_PROMPT}\\n\\nUSER: {user_text}"
        )
        ai_reply = response.text
        learning_engine.save_memory(user_text, ai_reply)
        return {"status": "success", "response": ai_reply}
    except Exception as e:
        return {"status": "error", "response": f"[JARVIS ERROR]: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
'''

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(backend_fix)

print("[SUCCESS] Autonomous File Reading & Direct Local Modification Enabled!")