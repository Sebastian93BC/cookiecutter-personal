import logging
from pathlib import Path

import pandas as pd

from src.utils.paths import data_raw_dir, models_dir
from src.utils.general_functions import Utils
from src.models.models import Models

logger = logging.getLogger(__name__)


def train(data_path: str, target_col: str, drop_cols: list) -> None:
    """
    Pipeline de entrenamiento: carga datos, separa features/target,
    divide en train/test, y ejecuta la búsqueda de hiperparámetros.

    El mejor modelo se exporta automáticamente a models/.

    Args:
        data_path: Nombre del archivo de datos en data/raw/.
        target_col: Nombre de la columna objetivo.
        drop_cols: Columnas a eliminar antes del entrenamiento.

    Para extender con nuevos modelos, edita la clase Models en models.py
    y añade nuevos estimadores a self.reg y sus hiperparámetros a self.param.
    """
    utils = Utils()

    # Cargar datos
    df = utils.load_dataset(data_raw_dir(data_path))

    # Separar features y target
    X, y = utils.features_target(df, drop_cols=drop_cols, y=target_col)

    # Dividir en train/test
    X_train, X_test, y_train, y_test = utils.split_data(X, y)

    # Escalar datos
    X_train_scaled, X_test_scaled = utils.process_and_scale_data(X_train, X_test)

    # Entrenar y exportar mejor modelo
    models = Models()
    models.grid_training(X_train_scaled, y_train)

    logger.info("Pipeline de entrenamiento completado.")


if __name__ == "__main__":
    # Ejemplo de uso — modifica según tu dataset
    train(
        data_path="dataset.csv",
        target_col="target",
        drop_cols=["target", "id"],
    )
