# -*- coding: utf-8 -*-
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
