# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}
  
## Installation guide

Please read [install.md](install.md) for details on how to set up this project.

## Project Organization

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
Project based on the [cookiecutter conda data science project template](https://github.com/jvelezmagic/cookiecutter-conda-data-science).