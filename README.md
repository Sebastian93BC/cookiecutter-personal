# Cookiecutter Conda Data Science

<div align="center">

[![Version](https://img.shields.io/badge/version-0.2.0-blue?style=for-the-badge&logo=gitbook&logoColor=white)](https://github.com/Sebastian93BC/cookiecutter-personal) [![Python 3.11+](https://img.shields.io/badge/Python-3.11+-brightgreen?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE.md) [![Cookiecutter](https://img.shields.io/badge/Cookiecutter-Template-lightgrey?style=for-the-badge&logo=cookiecutter&logoColor=white)](http://cookiecutter.readthedocs.org/)

</div>

> _A logical, reasonably standardized, but flexible project structure for doing and sharing data science work._

---

## ✨ Why This Template?

- **📁 Organized structure** — Clear separation of concerns across data, models, features, and visualizations
- **🔄 Reproducible** — Conda environments ensure consistency across teams and machines
- **⚡ Production-ready** — Optional CI/CD, pre-commit hooks, and testing scaffolding
- **🎯 Flexible** — Choose your scope (exploratory or production), packages level, and optional tools
- **🤖 AI-friendly** — Built-in VS Code settings for Copilot and intelligent agents

---

## 🚀 Quick Start

### Prerequisites

| Tool | Link | Comment |
|------|------|----------|
| 🐍 Conda or Mamba | [Download](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html) | Package manager for dependencies |
| 🍪 Cookiecutter | `pip install cookiecutter` | Template generator |

### Generate Your Project

```bash
# Interactive setup (customize all options)
cookiecutter template-data-science-base

# Or from GitHub
cookiecutter https://github.com/Sebastian93BC/cookiecutter-personal

# Quick generation with defaults
cookiecutter template-data-science-base --no-input
```

---

## ⚙️ Template Configuration

Customize your project during setup:

| Option | Choices | ℹ️ Description |
|--------|---------|----------------|
| **`project_scope`** | `exploratory` / `production` | Production includes CI/CD, pre-commit, pytest |
| **`project_packages`** | `All` / `Minimal` | All: advanced ML packages; Minimal: core only |
| **`use_dvc`** | `no` / `yes` | Enable data version control with DVC |
| **`use_uv`** | `no` / `yes` | Document `uv` as alternative to conda |
| **`python_version`** | `3.11` (default) | Python version for the environment |
| **`remote_url`** | Empty or GitHub URL | Auto-configure git remote on generation |

---

## 🗂️ Project Structure

```
📦 your-project/
├── 📄 LICENSE                          MIT license (configurable)
├── ⚙️  environment.yml                 Conda environment spec
├── 📋 README.md                        Project documentation
├── 📚 install.md                       Setup instructions
├── 🔧 pyproject.toml                   Project metadata & tool config
├── 📋 tasks.py                         Invoke task runner
│
├── 📁 data/                            Data directory structure
│   ├── external/                       Third-party data sources
│   ├── raw/                            Original, immutable data
│   ├── interim/                        Intermediate transformations
│   └── processed/                      Final datasets for modeling
│
├── 📁 src/                             **Source code** (the heart!)
│   ├── data/                           Data loading & processing
│   │   └── make_dataset.py
│   ├── features/                       Feature engineering
│   │   ├── build_features.py
│   │   └── feature_diagnostics.py
│   ├── models/                         Model training & prediction
│   │   ├── models.py
│   │   ├── train_model.py
│   │   └── predict_model.py
│   ├── utils/                          Utilities & helpers
│   │   ├── paths.py                    Project-relative path factory
│   │   └── general_functions.py        Utils class for ML workflows
│   └── visualization/                  Plotting & reporting
│       └── visualize.py
│
├── 📒 notebooks/                       Jupyter notebooks
│   └── 00-manual-src.ipynb             End-to-end demo with synthetic data
│
├── 📊 reports/                         Generated analysis & exports
│   └── figures/                        Plots & visualizations
│
├── 🧪 tests/                           Unit tests
│   ├── conftest.py
│   └── test_paths.py
│
├── 📎 references/                      Data dictionaries & manuals
└── ⚙️  config/
    └── config.yml                      Central configuration file
```

---

## 📚 Key Features

### 🤖 Smart IDE Setup
- Auto-detects `platzi_machine_learning` environment for template development
- Auto-selects project conda environment in generated projects
- Ready for Copilot, Pylance, and other intelligent assistants

### 📝 Battle-Tested Utilities

```python
from src.utils.paths import data_raw_dir, models_dir
from src.utils.general_functions import Utils
from src.features.build_features import describe_dataset
from src.visualization.visualize import plot_feature_importance
```

### 🎓 Learn by Example
- **`notebooks/00-manual-src.ipynb`** — Complete demo using synthetic sklearn data
- No real data needed to get started
- Covers all major modules and workflows

---

## 🤝 Contributing

All contributions are welcome!

- 🐛 Found a bug? Open an issue
- 💡 Have an idea? Share it!
- 📝 Improve docs? Send a PR
- ✨ Add features? We'd love to see them

---

## 📖 Credits & Inspiration

This template builds on and is influenced by:

- [**Cookiecutter Data Science**](https://github.com/drivendata/cookiecutter-data-science) by DrivenData
- [**Cookiecutter Kaggle**](https://github.com/andfanilo/cookiecutter-kaggle) by Andfanilo
- [**DrWatson**](https://juliadynamics.github.io/DrWatson.jl/dev/) — Julia's scientific project assistant

**Further Reading:**
- [Write less terrible code with Jupyter](https://blog.godatadriven.com/write-less-terrible-notebook-code)
- [Cookiecutter Data Science Opinions](http://drivendata.github.io/cookiecutter-data-science/#opinions)

---

<div align="center">

**Made with ❤️ for data scientists** | [Read the Docs](https://github.com/Sebastian93BC/cookiecutter-personal)

</div>

    ├── LICENSE
    ├── tasks.py           <- Invoke with commands like `invoke lab`.
    ├── README.md          <- The top-level README for developers using this project.
    ├── install.md         <- Detailed instructions to set up this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries.
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting.
    │
    ├── config             <- Configuration files (YAML).
    │   └── config.yml
    │
    ├── tests              <- Unit tests.
    │   ├── conftest.py
    │   └── test_paths.py
    │
    ├── environment.yml    <- Conda environment specification.
    │
    ├── pyproject.toml     <- Project metadata and tool configuration (PEP 621).
    │
    ├── .here              <- File that will stop the search if none of the other criteria
    │                         apply when searching head of project.
    │
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module.
        │
        ├── data           <- Scripts to download or generate data.
        │   └── make_dataset.py
        │
        ├── features       <- Scripts to turn raw data into features for modeling.
        │   ├── build_features.py
        │   └── feature_diagnostics.py
        │
        ├── models         <- Scripts to train models and then use trained models to make
        │   │                 predictions.
        │   ├── models.py
        │   ├── predict_model.py
        │   └── train_model.py
        │
        ├── utils          <- Scripts to help with common tasks.
        │   ├── paths.py   <- Helper functions to relative file referencing across project.
        │   └── general_functions.py
        │
    └── visualization  <- Scripts to create exploratory and results oriented visualizations.
        └── visualize.py

---

## Contributing guide

All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.

## Credits

This project is heavily influenced by [drivendata's Cookiecutter Data Science](https://github.com/drivendata/cookiecutter-data-science), [andfanilo's Cookiecutter for Kaggle Conda projects](https://github.com/andfanilo/cookiecutter-kaggle), and julia's package [DrWatson](https://juliadynamics.github.io/DrWatson.jl/dev/).

Other links that helped shape this cookiecutter :

- [Write less terrible code with Jupyter Notebook](https://blog.godatadriven.com/write-less-terrible-notebook-code)
- [Cookiecutter DataScience Opinions](http://drivendata.github.io/cookiecutter-data-science/#opinions)
