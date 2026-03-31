# Changelog

All notable changes to **{{ cookiecutter.project_name }}** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [{{ cookiecutter.project_version }}] - {% now 'utc', '%Y-%m-%d' %}

### Added

- Initial project structure generated from [Cookiecutter Conda Data Science](https://github.com/Sebastian93BC/cookiecutter-personal)
- Source modules: `data`, `features`, `models`, `utils`, `visualization`
- Conda environment (`environment.yml`)
- Demo notebook (`notebooks/00-manual-src.ipynb`)
- Project configuration (`config/config.yml`)
- Invoke task runner (`tasks.py`)
