import logging
from pathlib import Path

import joblib
import pandas as pd
import numpy as np

from src.utils.paths import models_dir

logger = logging.getLogger(__name__)


def load_model(model_filename: str):
    """
    Carga un modelo serializado desde models/.

    Args:
        model_filename: Nombre del archivo del modelo (e.g. 'best_model_abc123.pkl').

    Returns:
        El modelo deserializado.
    """
    model_path = models_dir(model_filename)
    model = joblib.load(model_path)
    logger.info(f"Modelo cargado desde: {model_path}")
    return model


def predict(model_filename: str, X: pd.DataFrame) -> np.ndarray:
    """
    Genera predicciones con un modelo guardado.

    Args:
        model_filename: Nombre del archivo del modelo en models/.
        X: DataFrame con las features de entrada.

    Returns:
        Array de predicciones.
    """
    model = load_model(model_filename)
    predictions = model.predict(X)
    logger.info(f"Predicciones generadas: {len(predictions)} muestras")
    return predictions
