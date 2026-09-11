# -*- coding: utf-8 -*-
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
