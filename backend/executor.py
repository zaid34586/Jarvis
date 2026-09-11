# -*- coding: utf-8 -*-
import subprocess
import sys
import os

def run_python_code(code_string: str) -> dict:
    """Runs generated Python code inside a sandboxed temp file and captures output/errors."""
    temp_filename = "temp_execution.py"
    try:
        with open(temp_filename, "w", encoding="utf-8") as f:
            f.write(code_string)
        
        result = subprocess.run(
            [sys.executable, temp_filename],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        
        if result.returncode == 0:
            return {"status": "success", "output": stdout or "Code executed with no output."}
        else:
            return {"status": "error", "error": stderr or "Unknown execution error."}

    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "Execution timed out (Limit: 15s)."}
    except Exception as e:
        return {"status": "error", "error": str(e)}
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
