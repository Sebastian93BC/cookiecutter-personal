# {{ cookiecutter.project_name }}
{% if cookiecutter.add_readme_header == "yes" %}
<div align="center">

**🌐 Social Media**

{% if cookiecutter.social_youtube_url and cookiecutter.social_youtube_channel_id %}[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/{{ cookiecutter.social_youtube_channel_id }}?style=for-the-badge&logo=youtube&logoColor=white&color=red)]({{ cookiecutter.social_youtube_url }}) {% endif %}{% if cookiecutter.social_github_username %}[![GitHub followers](https://img.shields.io/github/followers/{{ cookiecutter.social_github_username }}?style=for-the-badge&logo=github&logoColor=white)](https://github.com/{{ cookiecutter.social_github_username }}) {% endif %}{% if cookiecutter.social_linkedin_url %}[![LinkedIn Follow](https://img.shields.io/badge/LinkedIn-Follow-blue?style=for-the-badge&logo=linkedin&logoColor=white)]({{ cookiecutter.social_linkedin_url }}) {% endif %}{% if cookiecutter.social_x_url %}[![X Follow](https://img.shields.io/badge/X-Follow-black?style=for-the-badge&logo=x&logoColor=white)]({{ cookiecutter.social_x_url }}){% endif %}

</div>

{% endif %}
<div align="center">

[![Version](https://img.shields.io/badge/version-{{ cookiecutter.project_version }}-blue?style=for-the-badge&logo=gitbook&logoColor=white)]() [![Status](https://img.shields.io/badge/status-active-limegreen?style=for-the-badge)]() [![Python](https://img.shields.io/badge/Python-{{ cookiecutter.python_version | default('3.11') }}+-brightgreen?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) [![Conda](https://img.shields.io/badge/Conda-environment-lightblue?style=for-the-badge&logo=conda&logoColor=white)](environment.yml)
{% if cookiecutter.project_open_source_license != 'No license file' -%}
[![License](https://img.shields.io/badge/license-{{ cookiecutter.project_open_source_license }}-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
{% endif -%}

</div>

> {{ cookiecutter.project_description }}

---

## 🚀 Quick Start

### 1️⃣ Setup Environment

```bash
conda env create --file environment.yml
conda activate {{ cookiecutter.project_slug }}
```

### 2️⃣ Explore the Demo

```bash
jupyter lab notebooks/00-manual-src.ipynb
```

### 3️⃣ Add Your Data

```bash
# Place raw data in:
data/raw/your_dataset.csv
```

---

## 📁 Directory Guide

| Folder | Purpose | Example |
|--------|---------|----------|
| **`data/raw/`** | 🗄️ Original, immutable data | `customer_data.csv` |
| **`data/processed/`** | 🔄 Cleaned & ready for ML | `features_train.parquet` |
| **`src/features/`** | ⚙️ Feature engineering code | `build_features.py` |
| **`src/models/`** | 🤖 Model training & prediction | `train_model.py` |
| **`notebooks/`** | 📕 Analysis & experiments | `01-eda.ipynb` |
| **`reports/`** | 📊 Final outputs | `figures/`, `analysis.html` |
| **`tests/`** | 🧪 Unit tests | `test_models.py` |

---

## 📚 Project Organization

```
📦 {{ cookiecutter.project_slug }}/
├── 📋 README.md                    ← You are here!
├── 📄 LICENSE                      {{ cookiecutter.project_open_source_license | default('MIT') }} license
├── ⚙️  environment.yml             Conda environment definition
├── 📝 install.md                   Detailed setup instructions
├── 🔧 pyproject.toml               Project metadata
├── 📋 tasks.py                     Invoke commands
│
├── 📁 data/
│   ├── external/                   📥 Third-party sources
│   ├── raw/                        🗄️  Raw, untouched data
│   ├── interim/                    🔄 Intermediate transformations
│   └── processed/                  ✅ Final, clean datasets
│
├── 📁 src/                         **Core Python code**
│   ├── data/                       📥 Data loading utilities
│   ├── features/                   ⚙️  Feature engineering
│   ├── models/                     🤖 ML models & training
│   ├── utils/                      🛠️  Helper functions
│   └── visualization/              📊 Plotting & analysis
│
├── 📘 notebooks/
│   ├── 00-manual-src.ipynb         🧪 Demo with synthetic data
│   ├── 01-eda.ipynb                📊 Your EDA notebook
│   └── 02-modeling.ipynb           🤖 Your modeling notebook
│
├── 📊 reports/
│   ├── figures/                    📈 Plots & visualizations
│   └── analysis.html               📄 Final reports
│
├── 🧪 tests/
│   └── test_models.py              Unit tests for code
│
├── 📎 references/                  📖 Data dictionaries, manuals
│
└── ⚙️  config/
    └── config.yml                  Central configuration
```

---

## 💡 Usage Examples

### Load Your Data

```python
from src.utils.general_functions import Utils
from src.utils.paths import data_raw_dir

utils = Utils()
df = utils.load_dataset(data_raw_dir('my_data.csv'))
print(f"Loaded {df.shape[0]} rows, {df.shape[1]} columns")
```

### Build Features

```python
from src.features.build_features import describe_dataset

summary = describe_dataset(df)
print(summary['quantitative'])
```

### Train a Model

```python
from src.models.models import Models

models = Models()
models.grid_training(X_train, y_train)  # Saved to models/ automatically
```

### Visualize Results

```python
from src.visualization.visualize import plot_feature_importance

fig = plot_feature_importance(
    feature_names=X.columns,
    importances=model.feature_importances_,
    save=True,
    filename='importance.png'
)
```

---

## 📖 Next Steps

- [ ] ✅ Read [install.md](install.md) for advanced setup
- [ ] 📊 Run `jupyter lab notebooks/00-manual-src.ipynb` to see all modules in action
- [ ] 📥 Add your data to `data/raw/`
- [ ] 🔄 Create feature engineering notebook
- [ ] 🤖 Train your first model
- [ ] 📈 Generate reports in `reports/`
- [ ] 🧪 Write tests in `tests/`

---

## 🏃 Run Tasks

Project includes Invoke task runner for common operations:

```bash
invoke --list                          # Show all tasks
invoke lab                             # Start Jupyter Lab
invoke test                            # Run unit tests
```

---

## 📞 Need Help?

**Quick References:**
- 🔗 [Conda Documentation](https://docs.conda.io/)
- 🔭 [Jupyter Lab Guide](https://jupyterlab.readthedocs.io/)
- 🤖 [Scikit-Learn API](https://scikit-learn.org/)
- 📊 [Pandas Cheatsheet](https://pandas.pydata.org/docs/)

---
{% if cookiecutter.add_readme_footer == "yes" %}

## 💬 ¿Tienes dudas o sugerencias?

- 💭 **YouTube**: comentarios por capítulo
- 🐛 **GitHub Issues**: bugs y mejoras al código
- 💼 **LinkedIn/X**: conversaciones sobre IA y desarrollo

**¡Suscríbete para no perderte nada!** 🔔

---

<div align="center">

### 🎯 ¿Te ha resultado útil este contenido?

{% if cookiecutter.social_linkedin_url %}
[![Conecta en LinkedIn](https://img.shields.io/badge/💼%20CONECTA%20EN%20LINKEDIN-blue?style=for-the-badge&logo=linkedin&logoColor=white)]({{ cookiecutter.social_linkedin_url }})
{% endif %}
¡Nos vemos 👋🏻!

</div>

---

{% endif %}
## 📝 Project Information

**Version:** `{{ cookiecutter.project_version }}`  
**Python:** `{{ cookiecutter.python_version }}+`  
**Author:** {{ cookiecutter.project_author_name }}  
**Email:** {{ cookiecutter.project_author_email }}

---

<div align="center">

**Created from 📊 [Cookiecutter Conda Data Science](https://github.com/Sebastian93BC/cookiecutter-personal)**

</div>