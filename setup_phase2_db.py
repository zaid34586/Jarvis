import os

mongo_engine_code = '''# -*- coding: utf-8 -*-
import json
import os
from typing import List, Dict
from pymongo import MongoClient

# Local fallback file
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "jarvis_memory.json")

# MongoDB Setup (Optional Cloud URI from environment)
MONGO_URI = os.getenv("MONGO_URI", "")
db_client = None
collection = None

if MONGO_URI:
    try:
        db_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        db = db_client["jarvis_db"]
        collection = db["memories"]
        print("[DATABASE]: Connected to Cloud MongoDB!")
    except Exception as e:
        print(f"[DATABASE WARNING]: Cloud MongoDB failed, falling back to local storage: {e}")

def load_memory() -> List[Dict[str, str]]:
    if collection is not None:
        try:
            memories = list(collection.find({}, {"_id": 0}))
            return memories
        except Exception:
            pass

    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_memory(user_prompt: str, ai_response: str):
    memory_entry = {"prompt": user_prompt, "response": ai_response}
    
    # Save to MongoDB if available
    if collection is not None:
        try:
            collection.insert_one(memory_entry.copy())
        except Exception as e:
            print(f"[DATABASE ERROR]: MongoDB save failed: {e}")

    # Fallback/Dual save to local JSON file
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
    f.write(mongo_engine_code)

print("[SUCCESS] Phase 2: MongoDB & Memory Storage Engine Successfully Integrated!")