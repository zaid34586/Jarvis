import subprocess
import sys
import time
import os

def start_system():
    print("[SYSTEM] Starting JARVIS Unified Neural Engine...")
    
    # Start Backend Process
    backend_cmd = [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"]
    backend_process = subprocess.Popen(backend_cmd, cwd=os.path.join(os.getcwd(), "backend"))
    print("[BACKEND] Fast API Core started on port 8000.")

    # Start Frontend Process
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    frontend_process = subprocess.Popen([npm_cmd, "run", "dev"], cwd=os.path.join(os.getcwd(), "frontend"))
    print("[FRONTEND] React Vite Dev Server started on port 5173.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[SYSTEM] Shutting down JARVIS Core...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    start_system()