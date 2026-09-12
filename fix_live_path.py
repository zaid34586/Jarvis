import os

engine_file = "backend/self_code_engine.py"

if os.path.exists(engine_file):
    with open(engine_file, "r", encoding="utf-8") as f:
        code = f.read()

    old_target = "target_path = os.path.abspath(os.path.join(PROJECT_ROOT, relative_path))"
    new_target = """clean_path = relative_path.replace("src/App.jsx", "frontend/src/App.jsx") if "frontend/" not in relative_path and "App.jsx" in relative_path else relative_path
        target_path = os.path.abspath(os.path.join(PROJECT_ROOT, clean_path))"""

    if old_target in code:
        code = code.replace(old_target, new_target)
        with open(engine_file, "w", encoding="utf-8") as f:
            f.write(code)
        print("[SUCCESS] Live Path Resolver Fixed Successfully!")
    else:
        print("[INFO] Path resolver logic already present or structure updated.")