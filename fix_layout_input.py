import os

agent_code = '''# -*- coding: utf-8 -*-
import os
from google import genai
from dotenv import load_dotenv
import self_code_engine
import learning_engine

load_dotenv(override=True)

class AutonomousAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    def run_task(self, user_goal: str):
        if not self.client:
            return {"status": "error", "summary": "Gemini API Key missing."}

        system_prompt = """You are JARVIS Autonomous Core.
Generate valid React JSX code for App.jsx.

STRICT MANDATORY RULES:
1. Always apply dark background (#030712) and cyan text styling inline (`style={{ backgroundColor: '#030712', color: '#00f3ff', fontFamily: 'monospace' }}`). Do NOT use Tailwind CSS classes.
2. You MUST include a fixed command input bar at the bottom with a form that posts user input to `http://127.0.0.1:8000/api/process` so the user can continue executing commands.
3. Output ONLY valid React JSX code starting with import statements and ending with export default.
"""

        prompt = f"{system_prompt}\\n\\nUSER GOAL: {user_goal}"

        try:
            response = self.client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt
            )
            raw_code = response.text.strip()

            if "```" in raw_code:
                parts = raw_code.split("```")
                for p in parts:
                    if "import React" in p or "export default" in p:
                        raw_code = p.replace("jsx", "").replace("javascript", "").strip()
                        break

            if "import React" in raw_code or "export default" in raw_code:
                filepath = os.path.abspath("frontend/src/App.jsx")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(raw_code)

                learning_engine.save_memory(user_goal, "Patched App.jsx with preserved control console.")
                return {
                    "status": "success",
                    "summary": "Live code patched with Dark Theme & Command Console preserved.",
                    "code": raw_code
                }
            return {"status": "error", "summary": "Invalid React structure."}

        except Exception as e:
            return {"status": "error", "summary": f"Agent error: {str(e)}"}

agent = AutonomousAgent()
'''

with open("backend/agent_loop.py", "w", encoding="utf-8") as f:
    f.write(agent_code)

print("[SUCCESS] Applied Dark Styling & Command Console Protection!")