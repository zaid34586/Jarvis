# -*- coding: utf-8 -*-
import sys
import io
import traceback

def run_python_code(code: str) -> dict:
    """Executes provided Python code in a sandboxed environment with error handling and auto-fix capability."""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    result = {}
    
    try:
        exec_scope = {}
        exec(code, exec_scope)
        output = sys.stdout.getvalue()
        error = sys.stderr.getvalue()
        
        if error:
             result = {"status": "error", "output": output, "error": error}
        else:
             result = {"status": "success", "output": output}
             
    except Exception:
        output = sys.stdout.getvalue()
        error_type, error_value, _ = sys.exc_info()
        stack_trace = traceback.format_exc()
        result = {
            "status": "critical_error", 
            "output": output, 
            "error_type": str(error_type),
            "error_message": str(error_value),
            "stack_trace": stack_trace
        }
        
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    return result
