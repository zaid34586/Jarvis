import os

api_index_code = '''# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from main import app
'''

os.makedirs("api", exist_ok=True)
with open("api/index.py", "w", encoding="utf-8") as f:
    f.write(api_index_code)

print("[SUCCESS] Vercel Serverless Entrypoint Updated!")