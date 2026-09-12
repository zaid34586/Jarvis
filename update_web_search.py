import os

web_search_code = '''# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

def live_web_search(query: str, max_results: int = 4) -> str:
    """Performs real-time web search and returns aggregated search context."""
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(f"Title: {r.get('title')}\\nSnippet: {r.get('body')}\\nURL: {r.get('href')}\\n")
        
        if not results:
            return "No relevant web search results found."
        
        return "\\n---\\n".join(results)
    except Exception as e:
        return f"[SEARCH ERROR]: Failed to execute live web search: {str(e)}"

def fetch_web_page_content(url: str) -> dict:
    """Fetches raw text content from a given web page."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator=' ')
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = ' '.join(chunk for chunk in chunks if chunk)
            return {"status": "success", "content": clean_text[:3000]}
        else:
            return {"status": "error", "message": f"HTTP Error {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
'''

with open("backend/web_engine.py", "w", encoding="utf-8") as f:
    f.write(web_search_code)

print("[SUCCESS] Web Engine upgraded with Live Real-Time Internet Search!")