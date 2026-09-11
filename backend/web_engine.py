# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

def fetch_web_page_content(url: str) -> dict:
    """Fetches and extracts clean text and all links from a website URL.
       Designed for autonomous analysis and data extraction."""
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
