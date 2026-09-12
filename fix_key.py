import os

main_py_path = "backend/main.py"

if os.path.exists(main_py_path):
    with open(main_py_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure override=True is used for loading .env correctly
    if 'load_dotenv()' in content:
        content = content.replace('load_dotenv()', 'load_dotenv(override=True)')

    if 'client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key"))' in content:
        content = content.replace(
            'client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key"))',
            'api_key = os.getenv("OPENAI_API_KEY")\nclient = OpenAI(api_key=api_key)'
        )

    with open(main_py_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("[SUCCESS] backend/main.py successfully updated to load API key!")
else:
    print("[ERROR] backend/main.py not found!")