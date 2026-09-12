# -*- coding: utf-8 -*-
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def write_project_file(relative_path: str, new_content: str) -> dict:
    try:
        target_path = os.path.abspath(os.path.join(PROJECT_ROOT, relative_path))
        if not target_path.startswith(PROJECT_ROOT):
            return {"status": "error", "message": "Security Error: Attempted to write outside project root."}
        
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return {"status": "success", "message": f"File {relative_path} updated successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def read_project_file(relative_path: str) -> dict:
    try:
        target_path = os.path.abspath(os.path.join(PROJECT_ROOT, relative_path))
        if not os.path.exists(target_path):
            return {"status": "error", "message": f"File {relative_path} not found."}
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"status": "success", "content": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}