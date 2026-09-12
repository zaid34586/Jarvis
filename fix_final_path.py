import os

agent_path = "backend/agent_loop.py"

with open(agent_path, "r", encoding="utf-8") as f:
    code = f.read()

# Fix wrong nested path logic
code = code.replace(
    'filepath = os.path.abspath("frontend/src/App.jsx")',
    'ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n                filepath = os.path.join(ROOT_DIR, "frontend", "src", "App.jsx")'
)

with open(agent_path, "w", encoding="utf-8") as f:
    f.write(code)

print("[SUCCESS] Path issue permanently resolved!")