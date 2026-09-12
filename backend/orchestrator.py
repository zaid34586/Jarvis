# -*- coding: utf-8 -*-
import re

def analyze_intent(user_input: str) -> str:
    """Analyzes user input and determines the optimal tool/execution path."""
    text = user_input.lower()
    
    # Check for Web Scraping / Fetching Intent
    if any(k in text for k in ["http://", "https://", "fetch page", "scrape"]):
        return "WEB_SCRAPE"
        
    # Check for Python Execution / Code Sandbox Intent
    if "def " in text or "import " in text or "print(" in text or "run code" in text:
        return "EXECUTE_CODE"
        
    return "LLM_CHAT"
