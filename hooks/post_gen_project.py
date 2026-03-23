import os
import shutil
import subprocess

MESSAGE_COLOR = "\x1b[34m"
WARN_COLOR = "\x1b[33m"
RESET_ALL = "\x1b[0m"

# Remove license file if not selected
if "{{ cookiecutter.project_open_source_license }}" == "No license file":
    os.remove("LICENSE")

# Remove DVC files if not selected
if "{{ cookiecutter.use_dvc }}" == "no":
    for f in [".dvcignore"]:
        if os.path.exists(f):
            os.remove(f)

# Remove CI/CD if scope is exploratory
if "{{ cookiecutter.project_scope }}" == "exploratory":
    if os.path.exists(".github"):
        shutil.rmtree(".github")
    if os.path.exists(".pre-commit-config.yaml"):
        os.remove(".pre-commit-config.yaml")

# Initialize git repository
if shutil.which("git"):
    print(f"{MESSAGE_COLOR}Almost done!")
    print(f"Initializing a git repository...{RESET_ALL}")

    subprocess.call(["git", "init"])
    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", "Initial commit"])

    remote_url = "{{ cookiecutter.remote_url }}"
    if remote_url.strip():
        subprocess.call(["git", "remote", "add", "origin", remote_url])
        print(f"{MESSAGE_COLOR}Remote 'origin' configured: {remote_url}{RESET_ALL}")

    print(f"{MESSAGE_COLOR}The beginning of your destiny is defined now! Create and have fun!{RESET_ALL}")
else:
    print(f"{WARN_COLOR}WARNING: git not found. Skipping repository initialization.")
    print(f"You can initialize it later with 'git init'.{RESET_ALL}")