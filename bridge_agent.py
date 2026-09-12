import os

main_code = '''# -*- coding: utf-8 -*-
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_loop import agent

app = FastAPI(title="Jarvis Autonomous Neural Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommandRequest(BaseModel):
    user_input: str

@app.post("/api/process")
def process_command(request: CommandRequest):
    result = agent.run_task(request.user_input)
    
    if isinstance(result, dict) and result.get("status") == "success":
        return {
            "status": "success",
            "response": result["summary"],
            "file_modified": True,
            "file_path": "frontend/src/App.jsx",
            "code_preview": result.get("code", "")
        }
    
    msg = result.get("summary") if isinstance(result, dict) else str(result)
    return {"status": "success", "response": msg}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
'''

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(main_code)

print("[SUCCESS] Main Backend Integrated with Autonomous Agent Router!")