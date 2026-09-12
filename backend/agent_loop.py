# -*- coding: utf-8 -*-
import os
import json
import re
from google import genai
from dotenv import load_dotenv
import learning_engine

load_dotenv(override=True)

class MultiFileAutonomousAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def resolve_path(self, relative_path: str) -> str:
        """Resolves target relative path to absolute local disk path safely."""
        clean_path = relative_path.lstrip("/\\")
        return os.path.abspath(os.path.join(self.root_dir, clean_path))

    def run_task(self, user_goal: str):
        if not self.client:
            return {"status": "error", "summary": "Gemini API Key missing."}

        system_prompt = """You are JARVIS - an Autonomous Full-Stack Software Engineer with Multi-File Access.
You can read, create, or update ANY file in the project (e.g., frontend/src/components/..., backend/main.py, etc.).

JSON Execution Actions:
1. To write/create a file:
{"action": "WRITE_FILE", "path": "frontend/src/components/Metrics.jsx", "content": "<FULL_CODE>"}

2. To update main App component:
{"action": "WRITE_FILE", "path": "frontend/src/App.jsx", "content": "<FULL_CODE>"}

Return ONLY a valid JSON action block. Do not write markdown commentary outside JSON."""

        prompt = f"{system_prompt}\n\nUSER GOAL: {user_goal}"

        try:
            response = self.client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt
            )
            raw_text = response.text.strip()

            # Extract JSON Action
            match = re.search(r'\{[^{}]*"action"[^{}]*\}', raw_text, re.DOTALL)
            action_data = None
            if match:
                try:
                    action_data = json.loads(match.group(0))
                except Exception:
                    pass

            # Direct Code Block fallback if JSON parsing skips
            if not action_data and ("import React" in raw_text or "export default" in raw_text):
                clean_code = raw_text
                if "```" in raw_text:
                    parts = raw_text.split("```")
                    for p in parts:
                        if "import React" in p or "export default" in p:
                            clean_code = p.replace("jsx", "").replace("javascript", "").strip()
                            break
                action_data = {
                    "action": "WRITE_FILE",
                    "path": "frontend/src/App.jsx",
                    "content": clean_code
                }

            if action_data and action_data.get("action") == "WRITE_FILE":
                target_rel_path = action_data.get("path", "frontend/src/App.jsx")
                content = action_data.get("content", "")

                full_disk_path = self.resolve_path(target_rel_path)
                os.makedirs(os.path.dirname(full_disk_path), exist_ok=True)

                with open(full_disk_path, "w", encoding="utf-8") as f:
                    f.write(content)

                learning_engine.save_memory(user_goal, f"Modified {target_rel_path}")
                return {
                    "status": "success",
                    "summary": f"Successfully written/updated target file: {target_rel_path}",
                    "file_path": target_rel_path,
                    "code": content
                }

            return {"status": "info", "summary": raw_text}

        except Exception as e:
            return {"status": "error", "summary": f"Multi-file Agent error: {str(e)}"}

agent = MultiFileAutonomousAgent()
