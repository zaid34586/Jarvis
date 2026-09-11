import os

vercel_json = """{
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": { "distDir": "dist" }
    },
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "api/index.py" },
    { "src": "/(.*)", "dest": "frontend/$1" }
  ]
}
"""

os.makedirs("api", exist_ok=True)

with open("vercel.json", "w", encoding="utf-8") as f:
    f.write(vercel_json)

with open("api/index.py", "w", encoding="utf-8") as f:
    f.write("from backend.main import app\n")

if os.path.exists("backend/requirements.txt"):
    with open("backend/requirements.txt", "r", encoding="utf-8") as src:
        content = src.read()
    with open("api/requirements.txt", "w", encoding="utf-8") as dst:
        dst.write(content)

print("[SUCCESS] Vercel monorepo configuration files generated!")