import logging
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from src.utils.paths import reports_figures_dir

logger = logging.getLogger(__name__)


def plot_feature_importance(
    feature_names,
    importances,
    title: str = "Feature Importance",
    save: bool = False,
    filename: str = "feature_importance.png",
) -> plt.Figure:
    """
    Genera un gráfico de barras de importancia de features.

    Args:
        feature_names: Nombres de las features.
        importances: Array de importancias (e.g. model.feature_importances_).
        title: Título del gráfico.
        save: Si True, guarda la figura en reports/figures/.
        filename: Nombre del archivo al guardar.

    Returns:
        Figura de matplotlib.
    """
    df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances,
    }).sort_values("importance", ascending=True)

    fig, ax = plt.subplots(figsize=(10, max(6, len(df) * 0.35)))
    sns.barplot(data=df, x="importance", y="feature", palette="viridis", ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Importance")
    fig.tight_layout()

    if save:
        output_path = reports_figures_dir(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        logger.info(f"Figura guardada: {output_path}")

    return fig


def plot_residuals(
    y_true,
    y_pred,
    title: str = "Residuals vs Fitted",
    save: bool = False,
    filename: str = "residuals.png",
) -> plt.Figure:
    """
    Genera un gráfico de residuos vs valores ajustados.

    Args:
        y_true: Valores reales.
        y_pred: Valores predichos.
        title: Título del gráfico.
        save: Si True, guarda la figura en reports/figures/.
        filename: Nombre del archivo al guardar.

    Returns:
        Figura de matplotlib.
    """
    residuals = np.array(y_true) - np.array(y_pred)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(y_pred, residuals, alpha=0.5, edgecolors="k", linewidths=0.5)
    ax.axhline(0, linestyle="--", color="red", linewidth=1)
    ax.set_xlabel("Fitted Values")
    ax.set_ylabel("Residuals")
    ax.set_title(title)
    fig.tight_layout()

    if save:
        output_path = reports_figures_dir(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        logger.info(f"Figura guardada: {output_path}")

    return fig
