# -*- coding: utf-8 -*-
import json
import os
from typing import List, Dict

LEARNING_FILE = "jarvis_memory.json"

def load_memory() -> List[Dict]:
    if not os.path.exists(LEARNING_FILE):
        return []
    try:
        with open(LEARNING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_memory(user_prompt: str, ai_response: str, feedback: str = "success"):
    memory = load_memory()
    entry = {
        "user_prompt": user_prompt,
        "ai_response": ai_response,
        "feedback": feedback
    }
    memory.append(entry)
    with open(LEARNING_FILE, "w", encoding="utf-8") as f:
        json.dump(memory[-50:], f, indent=2, ensure_ascii=False)

def get_learned_context() -> str:
    memory = load_memory()
    if not memory:
        return "No past learning context available."
    
    summary = "Past successful interactions and patterns:\n"
    for item in memory[-5:]:
        clean_resp = item['ai_response'][:100].replace("\n", " ")
        summary += f"- User requested: {item['user_prompt']} | Strategy used: {clean_resp}...\n"
    return summary
