# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-03-23

### Added
- Cookiecutter template with configurable fields: `project_name`, `project_slug`, `python_version`, `project_scope`, `use_dvc`, `use_uv`, `remote_url`
- `post_gen_project.py` hook: removes unused files based on selections, initializes git repo, optionally adds remote origin
- `pre_gen_project.py` hook: validates inputs before project generation
- `src/` package structure: `data/`, `features/`, `models/`, `utils/`, `visualization/`
- `src/utils/paths.py`: `make_dir_function` factory for type-safe project-relative paths
- `src/utils/general_functions.py`: `Utils` class — `load_dataset`, `features_target`, `split_data`, `process_and_scale_data`, `model_export`
- `src/features/build_features.py`: `describe_dataset`, `check_normality`, and feature engineering helpers
- `src/features/feature_diagnostics.py`: diagnostic utilities for feature quality
- `src/models/models.py`: `Models` class with `GridSearchCV` over SVR and GradientBoostingRegressor
- `src/models/train_model.py` / `predict_model.py`: training and inference entry points
- `src/visualization/visualize.py`: `plot_feature_importance` and `plot_residuals` helpers
- `environment.yml` (project-level): reproducible conda environment named after `project_slug`
- Root `environment.yml`: development environment for template contributors (`platzi_machine_learning`)
- `tasks.py`: Invoke task runner for common project commands
- `config/config.yml`: central project configuration file
- `pyproject.toml`: project metadata and tooling configuration (ruff)
- `tests/` scaffold: `conftest.py`, `test_paths.py`
- `notebooks/00-manual-src.ipynb`: end-to-end demo notebook using synthetic sklearn data
- `.vscode/settings.json` (root): auto-selects `platzi_machine_learning` interpreter for template development
- `.vscode/settings.json` (project): auto-selects `project_slug` conda env in generated projects
- `.github/copilot-instructions.md`: AI agent guidelines specific to this template

### Changed
- Root `environment.yml`: renamed env from `cookiecutter-conda-data-science` to `platzi_machine_learning`; removed `anaconda` channel
- Root `.gitignore`: added `notes.txt` (personal scratch file) and `.vscode/` (machine-specific settings)

[Unreleased]: https://github.com/Sebastian93BC/cookiecutter-personal/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Sebastian93BC/cookiecutter-personal/releases/tag/v0.1.0
