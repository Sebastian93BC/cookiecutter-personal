# Cookiecutter Conda Data Science

_A logical, reasonably standardized, but flexible project structure for doing and sharing data science work._

## Requirements

- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html) or [Mamba](https://mamba.readthedocs.io/en/latest/)
- [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html):

```bash
pip install cookiecutter
```

or

```bash
conda install -c conda-forge cookiecutter
```

## Create a new project

En terminal, desde donde quieras generar el proyecto:
```bash
cookiecutter template-data-science-base
```

o si está publicado en GitHub:
```bash
cookiecutter https://github.com/jvelezmagic/cookiecutter-conda-data-science
```

### Template options

| Option | Values | Description |
|---|---|---|
| `project_packages` | All / Minimal | Include extended ML packages or keep it lean |
| `project_scope` | exploratory / production | Production adds pre-commit, pytest, and GitHub Actions CI |
| `use_dvc` | no / yes | Add DVC for data version control |
| `use_uv` | no / yes | Document uv/pip as an alternative to Conda |

## Resulting directory structure

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

## Contributing guide

All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.

## Credits

This project is heavily influenced by [drivendata's Cookiecutter Data Science](https://github.com/drivendata/cookiecutter-data-science), [andfanilo's Cookiecutter for Kaggle Conda projects](https://github.com/andfanilo/cookiecutter-kaggle), and julia's package [DrWatson](https://juliadynamics.github.io/DrWatson.jl/dev/).

Other links that helped shape this cookiecutter :

- [Write less terrible code with Jupyter Notebook](https://blog.godatadriven.com/write-less-terrible-notebook-code)
- [Cookiecutter DataScience Opinions](http://drivendata.github.io/cookiecutter-data-science/#opinions)
