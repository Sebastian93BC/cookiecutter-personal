import os
import re
import sys

project_slug = "{{ cookiecutter.project_slug }}"

ERROR_COLOR = "\x1b[31m"
MESSAGE_COLOR = "\x1b[34m"
RESET_ALL = "\x1b[0m"

if not re.match(r'^[a-z][a-z0-9_]+$', project_slug):
    print(f"{ERROR_COLOR}ERROR: '{project_slug}' is not a valid project slug.")
    print(f"It must start with a lowercase letter and contain only lowercase letters, digits, and underscores.{RESET_ALL}")
    sys.exit(1)

print(f"{MESSAGE_COLOR}Let's do it! You're going to create something awesome!")
print(f"Creating project at {os.getcwd()}{RESET_ALL}")