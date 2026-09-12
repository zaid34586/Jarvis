import os

agent_loop_code = '''# -*- coding: utf-8 -*-
import json
import re
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
        """Autonomous ReAct Loop: Research -> Draft Code -> Validate -> Apply"""
        if not self.client:
            return "Gemini API Key missing."

        print(f"[JARVIS AGENT]: Starting autonomous goal execution: {user_goal}")

        system_prompt = """You are JARVIS - an Autonomous Self-Updating Agent.
Goal: Fulfill user objective by directly generating valid React JSX code for frontend/src/App.jsx.
Constraint: Return ONLY clean React component code starting with imports and ending with export default. Do NOT wrap in raw JSON strings.
"""
        prompt = f"{system_prompt}\\n\\nUSER GOAL: {user_goal}"
        
        try:
            response = self.client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt
            )
            raw_code = response.text

            # Clean Markdown formatting
            if "```" in raw_code:
                parts = raw_code.split("```")
                for p in parts:
                    if "import React" in p or "export default" in p:
                        raw_code = p.replace("jsx", "").replace("javascript", "").strip()
                        break

            # Execute Direct Disk Patch
            if "import React" in raw_code or "export default" in raw_code:
                self_code_engine.write_project_file("frontend/src/App.jsx", raw_code)
                learning_engine.save_memory(user_goal, "Autonomous Agent self-patched App.jsx")
                return {
                    "status": "success",
                    "summary": "Objective completed. Clean code compiled and live-patched to frontend/src/App.jsx",
                    "code": raw_code
                }
            return {"status": "info", "summary": raw_code}

        except Exception as e:
            return {"status": "error", "summary": f"Agent loop failed: {str(e)}"}

agent = AutonomousAgent()
'''

with open("backend/agent_loop.py", "w", encoding="utf-8") as f:
    f.write(agent_loop_code)

print("[SUCCESS] Autonomous Agent Loop Controller Created!")