# -*- coding: utf-8 -*-
import time
import json
import threading
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)

class AutonomousBrain:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None
        self.is_learning = True

    def continuous_research_loop(self):
        """Background loop that autonomously learns patterns and updates memory."""
        while self.is_learning:
            try:
                # Simulating autonomous periodic learning cycles
                time.sleep(300) # Learn every 5 minutes automatically
                if self.client:
                    prompt = "Analyze modern software architecture trends for React and FastAPI. Summarize 1 core pattern to apply."
                    res = self.client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=prompt
                    )
                    # Persist learned knowledge
                    with open("backend/learned_knowledge.json", "a", encoding="utf-8") as f:
                        f.write(json.dumps({"timestamp": time.time(), "insight": res.text}) + "\n")
            except Exception as e:
                print(f"[BRAIN ERROR]: {str(e)}")
                time.sleep(60)

brain_node = AutonomousBrain()
