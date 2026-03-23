# 📝 Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased] 🚀

_Upcoming features and improvements in development._

---

## [0.2.0] - 2026-03-23

### ✨ Added

**Documentation & Licensing**
- 📜 `LICENSE.md` in template root (MIT)
- 📜 `LICENSE` template in generated projects (conditional: MIT, BSD-3-Clause, or none)
- 🎨 Badges in root `README.md`: version, Python requirement, license, cookiecutter
- 🎨 Badges in generated project `README.md`: version, Python requirement, Conda environment

**Developer Experience**
- 💻 `.vscode/settings.json` (root): auto-selects `platzi_machine_learning` interpreter
- 💻 `.vscode/settings.json` (generated projects): auto-selects `{{ cookiecutter.project_slug }}` environment
- 🤖 Ready for VS Code Copilot and intelligent agents

**Learning Resources**
- 📓 `notebooks/00-manual-src.ipynb`: 16-cell demo notebook with synthetic sklearn data
- 📚 Zero external dependencies — learn with built-in synthetic datasets

**Configuration Enhancement**
- 🔗 `{{ cookiecutter.remote_url }}` field in `cookiecutter.json`: optional git remote configuration
- 🎯 Auto-configure `git remote add origin <url>` during project generation

### 🔄 Changed

**Environment & Tooling**
- 🎯 Root `environment.yml`: renamed from `cookiecutter-conda-data-science` → `platzi_machine_learning`
- 🎯 Removed `anaconda` channel, kept only `conda-forge` + `defaults`
- 📝 `.github/copilot-instructions.md`: complete rewrite with template-specific guidelines
  - ❌ Removed incorrect Todo App documentation
  - ✅ Added accurate Jinja2 templating patterns
  - ✅ Added hook logic documentation
  - ✅ Added common task workflows

**Project Files**
- 🚫 `.gitignore` (root): added `notes.txt` (personal scratch files) + `.vscode/` (machine-specific)
- 🔧 `post_gen_project.py`: added conditional `git remote add origin` when `remote_url` is provided

---

## [0.1.0] - Initial Release

### ✨ Added

**Project Structure**
- 🗂️ Complete cookiecutter template with configurable fields
- 📁 `src/` package: organized into `data/`, `features/`, `models/`, `utils/`, `visualization/`
- 🎯 `src/utils/paths.py`: type-safe project-relative paths using `pyprojroot`
- 🛠️ `src/utils/general_functions.py`: `Utils` class for ML workflows
  - `load_dataset()`, `features_target()`, `split_data()`
  - `process_and_scale_data()`, `model_export()`

**Feature Engineering & Analysis**
- ⚙️ `src/features/build_features.py`: `describe_dataset()`, `check_normality()`
- 📊 `src/features/feature_diagnostics.py`: diagnostic utilities

**Model Training**
- 🤖 `src/models/models.py`: `Models` class with `GridSearchCV` tuning
- 📈 `src/models/train_model.py` / `predict_model.py`: training & inference entry points

**Visualization & Reporting**
- 📊 `src/visualization/visualize.py`: `plot_feature_importance()`, `plot_residuals()`

**Project Management**
- 🔧 `environment.yml`: reproducible conda environment
- 🔧 `pyproject.toml`: PEP 621 project metadata + ruff config
- 📋 `tasks.py`: Invoke task runner for common commands
- 🧪 `tests/` scaffold: `conftest.py`, `test_paths.py`
- 📚 `config/config.yml`: central configuration file

**Hooks for Generation**
- 🪝 `post_gen_project.py`: removes unused files, initializes git repo
- 🪝 `pre_gen_project.py`: input validation before generation

---

## Version History

| Version | Date | Release Notes |
|---------|------|---------------|
| v0.2.0 | 2026-03-23 | Enhanced DX, AI-ready, badges, licensing |
| v0.1.0 | Initial | Complete template with core functionality |

---

## 🔗 Links

- **GitHub:** [Sebastian93BC/cookiecutter-personal](https://github.com/Sebastian93BC/cookiecutter-personal)
- **Changelog:** [Compare v0.1.0...HEAD](https://github.com/Sebastian93BC/cookiecutter-personal/compare/v0.1.0...HEAD)

[Unreleased]: https://github.com/Sebastian93BC/cookiecutter-personal/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/Sebastian93BC/cookiecutter-personal/releases/tag/v0.2.0
[0.1.0]: https://github.com/Sebastian93BC/cookiecutter-personal/releases/tag/v0.1.0
