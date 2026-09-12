import os

self_code_module = '''# -*- coding: utf-8 -*-
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def write_project_file(relative_path: str, new_content: str) -> dict:
    """Allows Jarvis to safely edit or create files within the project codebase."""
    try:
        target_path = os.path.abspath(os.path.join(PROJECT_ROOT, relative_path))
        
        # Security Guardrail: Prevent modifying outside project folder
        if not target_path.startswith(PROJECT_ROOT):
            return {"status": "error", "message": "Access Denied: Path outside project scope."}
            
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        return {"status": "success", "message": f"Successfully updated file: {relative_path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def read_project_file(relative_path: str) -> dict:
    """Allows Jarvis to read existing source code to understand how to fix/upgrade it."""
    try:
        target_path = os.path.abspath(os.path.join(PROJECT_ROOT, relative_path))
        if not os.path.exists(target_path):
            return {"status": "error", "message": "File not found."}
            
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"status": "success", "content": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}
'''

with open("backend/self_code_engine.py", "w", encoding="utf-8") as f:
    f.write(self_code_module)

print("[SUCCESS] Self-Code Modification Engine successfully created!")