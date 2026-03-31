import os
import shutil
import subprocess

MESSAGE_COLOR = "\x1b[34m"
WARN_COLOR = "\x1b[33m"
RESET_ALL = "\x1b[0m"

# Copy .github from template root into the generated project
# Strategy 1: navigate up from this hook file's location (works when cookiecutter
# runs the hook from its original path in the template directory)
_hook_dir = os.path.dirname(os.path.abspath(__file__))
_template_github = os.path.join(os.path.dirname(_hook_dir), '.github')

# Strategy 2 (fallback): search sibling directories of the generated project
# for a folder that contains cookiecutter.json (= the template root)
if not os.path.isdir(_template_github):
    _parent = os.path.dirname(os.getcwd())
    for _sibling in os.listdir(_parent):
        _sibling_path = os.path.join(_parent, _sibling)
        if os.path.isdir(_sibling_path) and os.path.isfile(
            os.path.join(_sibling_path, 'cookiecutter.json')
        ):
            _candidate = os.path.join(_sibling_path, '.github')
            if os.path.isdir(_candidate):
                _template_github = _candidate
                break

if os.path.isdir(_template_github):
    shutil.copytree(_template_github, '.github', dirs_exist_ok=True)
    print(f"{MESSAGE_COLOR}Copied .github from template root.{RESET_ALL}")
else:
    print(f"{WARN_COLOR}WARNING: Could not find .github in template root. Skipping.{RESET_ALL}")

# Remove license file if not selected
if "{{ cookiecutter.project_open_source_license }}" == "No license file":
    os.remove("LICENSE")

# Remove DVC files if not selected
if "{{ cookiecutter.use_dvc }}" == "no":
    for f in [".dvcignore"]:
        if os.path.exists(f):
            os.remove(f)

# Remove pre-commit config if scope is exploratory
if "{{ cookiecutter.project_scope }}" == "exploratory":
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