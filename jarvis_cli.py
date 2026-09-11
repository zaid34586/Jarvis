# -*- coding: utf-8 -*-
import requests
import sys

API_URL = "http://127.0.0.1:8000"

def run_cli():
    print("==========================================")
    print("   JARVIS AUTONOMOUS CLI CONTROLLER       ")
    print("==========================================")
    print("Type 'exit' to quit.
")
    
    while True:
        try:
            user_input = input("Jarvis-CLI > ")
            if user_input.lower() in ["exit", "quit"]:
                break
            if not user_input.trim():
                continue
            
            res = requests.post(f"{API_URL}/api/process", json={"user_input": user_input})
            if res.status_code == 200:
                data = res.json()
                print(f"
[JARVIS]:
{data.get('response', '')}
")
            else:
                print(f"[ERROR]: Status code {res.status_code}")
        except Exception as e:
            print(f"[ERROR]: Connection failed ({str(e)})")

if __name__ == "__main__":
    run_cli()
