# {{ cookiecutter.project_name }} — Installation Guide

## Prerequisites

- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html) or [Mamba](https://mamba.readthedocs.io/en/latest/)

## Create environment

```bash
conda env create -f environment.yml
conda activate {{ cookiecutter.project_slug }}
```

or with Mamba (faster):

```bash
mamba env create -f environment.yml
mamba activate {{ cookiecutter.project_slug }}
```

{% if cookiecutter.use_uv == "yes" -%}
### Alternative: uv / pip

If you prefer not to use Conda:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
uv pip install -e ".[dev]"
```
{% endif -%}

## Install project module

Install the `src/` package in editable mode so you can import it from notebooks and scripts:

```bash
pip install --editable .
```

To auto-reload modules inside notebooks:

```python
%load_ext autoreload
%autoreload 2
```

Example usage:

```python
from src.utils.paths import data_raw_dir
data_raw_dir()
```

## Git diff for notebooks

We use [nbdime](https://nbdime.readthedocs.io/en/stable/index.html) for diffing and merging Jupyter notebooks.

```bash
nbdime config-git --enable
```

{% if cookiecutter.project_scope == "production" -%}
## Pre-commit hooks

This project uses [pre-commit](https://pre-commit.com/) to run linting and formatting checks before each commit.

```bash
pre-commit install
```

To run all hooks manually:

```bash
pre-commit run --all-files
```

{% endif -%}
## Invoke tasks

We use [Invoke](http://www.pyinvoke.org/) as a task runner.

```
$ invoke -l

Available tasks:

  clean       Remove Python file artifacts.
  format      Run ruff formatter on src/.
  lab         Launch Jupyter Lab.
  lint        Run ruff linter on src/.
  notebook    Launch Jupyter Notebook.
  test        Run pytest.
```

Task definitions live in `tasks.py` — add your own there.
