<!-- Auto-generated guidance for AI coding agents. -->
# Copilot / AI Agent Instructions — {{ cookiecutter.project_name }}

Goal: be immediately productive with this data science project.

- **Python package:** `src/` is the importable package.
- **Install:** create the conda env from `environment.yml` and run
  `pip install -e .` so modules import as `src.*`.
  See `install.md` for setup steps.

Key files & intent (read before coding):
- `README.md` — project layout and conventions.
- `install.md` — developer workflows: `conda env create -f environment.yml`,
  `pip install --editable .`, invoke tasks.
- `pyproject.toml` — project metadata, ruff config, pytest config.
- `tasks.py` — task runner (Invoke). Use `invoke -l` to list tasks.
- `src/utils/paths.py` — canonical way to build project-relative paths.
  Example: `from src.utils.paths import data_raw_dir; data_raw_dir()`
- `src/utils/general_functions.py` — `Utils` class for common ML operations.
- `src/features/build_features.py` — EDA, cleaning, transformation functions.
- `src/features/feature_diagnostics.py` — VIF, ANOVA, chi-squared analysis.
- `src/models/models.py` — `Models` class for model training with GridSearchCV.
- `src/models/train_model.py` / `predict_model.py` — training and prediction pipelines.
- `src/visualization/visualize.py` — reusable plotting helpers.
- `config/config.yml` — project configuration.

Patterns & conventions:
- Data layout: `data/raw`, `data/interim`, `data/processed`, `data/external`.
  Always use helpers from `src/utils/paths.py` for portability.
- Notebooks: follow naming convention in `README.md`, enable `%autoreload`.
- Package import: use `src.*` namespace.
- Linting: ruff (configured in `pyproject.toml`).
- Testing: pytest, tests live in `tests/`.

Developer commands:
- Create environment: `conda env create -f environment.yml`
- Activate: `conda activate {{ cookiecutter.project_slug }}`
- Install editable: `pip install -e .`
- Start notebook: `invoke lab` or `invoke notebook`
- Lint: `invoke lint` (with `--fix` for auto-fix)
- Format: `invoke format`
- Test: `invoke test`
- Clean artifacts: `invoke clean`

How to edit code:
- Prefer small, targeted changes within `src/`.
- Use `src/utils/paths.py` helpers for all file paths.
- Functions that produce plots should return `matplotlib.figure.Figure`
  objects, not call `plt.show()`.

Files to inspect before major changes:
- `install.md`, `README.md`, `pyproject.toml`, `tasks.py`,
  `src/utils/paths.py`, `src/features/build_features.py`.

End.
