import os

agent_fix = '''# -*- coding: utf-8 -*-
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

        system_prompt = """You are JARVIS. Build modern React components using inline styles or CSS.
IMPORTANT: You MUST preserve the bottom command input form with id="jarvis-command-form" so the user can continue giving instructions.
Output ONLY raw React JSX code for App.jsx. Do NOT include markdown blocks or extra text."""

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
                # Direct Disk Write to React File
                filepath = os.path.abspath("frontend/src/App.jsx")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(raw_code)

                learning_engine.save_memory(user_goal, "Patched App.jsx successfully")
                return {
                    "status": "success",
                    "summary": f"Live patch applied to App.jsx.",
                    "code": raw_code
                }
            return {"status": "error", "summary": "Invalid React code generated."}

        except Exception as e:
            return {"status": "error", "summary": f"Agent error: {str(e)}"}

agent = AutonomousAgent()
'''

with open("backend/agent_loop.py", "w", encoding="utf-8") as f:
    f.write(agent_fix)

print("[SUCCESS] Applied Disk Flush Enforcer!")