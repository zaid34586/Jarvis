import os

gitignore_content = """node_modules/
dist/
__pycache__/
*.pyc
.env
temp_execution.py
jarvis_memory.json
.vscode/
"""

dockerfile_backend = """FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
"""

docker_compose_content = """version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
"""

git_script_content = '''# -*- coding: utf-8 -*-
import subprocess
import os

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[OK] {cmd}")
        print(result.stdout.strip())
    else:
        print(f"[ERROR] {cmd}")
        print(result.stderr.strip())

def auto_git_push(commit_msg="Auto update from Jarvis Engine"):
    print("--- Starting Git Automation ---")
    run_cmd("git init")
    run_cmd("git add .")
    run_cmd(f'git commit -m "{commit_msg}"')
    print("Git repository localized and committed.")
    print("To push to GitHub, run: git remote add origin <YOUR_REPO_URL> && git push -u origin main")

if __name__ == "__main__":
    auto_git_push()
'''

package_script_content = '''# -*- coding: utf-8 -*-
import zipfile
import os

def zip_project(output_filename="jarvis_project_phase5.zip"):
    print(f"Creating project package: {output_filename}...")
    exclude_dirs = {"node_modules", "__pycache__", ".git", "dist"}
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as ziph:
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if file.endswith('.zip') or file == '.env':
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, ".")
                ziph.write(file_path, arcname)
    print(f"[SUCCESS] Package created successfully: {output_filename}")

if __name__ == "__main__":
    zip_project()
'''

# Write Deployment Artifacts
with open(".gitignore", "w", encoding="utf-8") as f:
    f.write(gitignore_content)

with open("backend/Dockerfile", "w", encoding="utf-8") as f:
    f.write(dockerfile_backend)

with open("docker-compose.yml", "w", encoding="utf-8") as f:
    f.write(docker_compose_content)

with open("git_deploy.py", "w", encoding="utf-8") as f:
    f.write(git_script_content)

with open("package_project.py", "w", encoding="utf-8") as f:
    f.write(package_script_content)

print("[SUCCESS] Phase 5 Deployment, Git Automation & Packaging Scripts generated!")