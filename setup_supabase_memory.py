import os

supabase_engine_code = '''# -*- coding: utf-8 -*-
import json
import os
from typing import List, Dict
from supabase import create_client, Client

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "jarvis_memory.json")

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

supabase: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("[DATABASE]: Connected to Supabase Cloud Memory!")
    except Exception as e:
        print(f"[DATABASE WARNING]: Supabase connection failed: {e}")

def load_memory() -> List[Dict[str, str]]:
    if supabase is not None:
        try:
            res = supabase.table("memories").select("prompt, response").order("created_at", desc=False).execute()
            return res.data
        except Exception as e:
            print(f"[DATABASE ERROR]: Load failed from Supabase: {e}")

    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_memory(user_prompt: str, ai_response: str):
    memory_entry = {"prompt": user_prompt, "response": ai_response}
    
    if supabase is not None:
        try:
            supabase.table("memories").insert(memory_entry).execute()
        except Exception as e:
            print(f"[DATABASE ERROR]: Supabase save failed: {e}")

    memories = load_memory()
    memories.append(memory_entry)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, indent=4, ensure_ascii=False)

def get_learned_context() -> str:
    memories = load_memory()
    if not memories:
        return "No prior memory stored."
    
    recent_memories = memories[-5:]
    context = ""
    for idx, mem in enumerate(recent_memories, 1):
        context += f"Memory {idx}: User asked '{mem.get('prompt')}' -> Jarvis responded '{mem.get('response')[:150]}...'\\n"
    return context
'''

with open("backend/learning_engine.py", "w", encoding="utf-8") as f:
    f.write(supabase_engine_code)

print("[SUCCESS] Backend Memory Engine successfully upgraded to Supabase Cloud!")