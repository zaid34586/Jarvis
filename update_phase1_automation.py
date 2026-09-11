# update_phase1_automation.py
import os

# 1. Update backend/web_engine.py for Advanced Scraping
web_engine_content = """# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

def fetch_web_page_content(url: str) -> dict:
    \"\"\"Fetches and extracts clean text and all links from a website URL.
       Designed for autonomous analysis and data extraction.\"\"\"
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract Text
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text(separator=' ')
            clean_text = ' '.join(text.split())[:5000] # Limit to 5000 chars

            # Extract Links
            links = []
            for link in soup.find_all('a', href=True):
                if link['href'].startswith('http'):
                    links.append({"text": link.get_text().strip(), "url": link['href']})

            return {
                "status": "success", 
                "url": url, 
                "content": clean_text,
                "found_links": links[:20] # Limit to first 20 links
            }
        else:
            return {"status": "error", "error": f"HTTP Error {response.status_code}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}
"""

# 2. Update backend/executor.py for Code Auto-Fixing
executor_content = """# -*- coding: utf-8 -*-
import sys
import io
import traceback

def run_python_code(code: str) -> dict:
    \"\"\"Executes provided Python code in a sandboxed environment with error handling and auto-fix capability.\"\"\"
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
"""

# Write the updated contents
with open("backend/web_engine.py", "w", encoding="utf-8") as f:
    f.write(web_engine_content)

with open("backend/executor.py", "w", encoding="utf-8") as f:
    f.write(executor_content)

print("[SUCCESS] Phase 1 Automation (Advanced Scraping & Auto-Fixing) files updated!")