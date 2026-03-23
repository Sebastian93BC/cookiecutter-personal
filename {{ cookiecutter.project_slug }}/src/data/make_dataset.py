import logging
from pathlib import Path

import pandas as pd

from src.utils.paths import data_raw_dir, data_processed_dir, data_interim_dir

logger = logging.getLogger(__name__)


def load_raw(filename: str) -> pd.DataFrame:
    """
    Carga un dataset crudo desde data/raw/.

    Args:
        filename: Nombre del archivo (e.g. 'dataset.csv').

    Returns:
        DataFrame con los datos crudos.
    """
    path = data_raw_dir(filename)
    df = pd.read_csv(path)
    logger.info(f"Dataset crudo cargado: {path} ({df.shape[0]} filas, {df.shape[1]} columnas)")
    return df


def save_processed(df: pd.DataFrame, filename: str) -> Path:
    """
    Guarda un dataset procesado en data/processed/.

    Args:
        df: DataFrame a guardar.
        filename: Nombre del archivo de salida (e.g. 'clean.csv').

    Returns:
        Path del archivo guardado.
    """
    output_path = data_processed_dir(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Dataset procesado guardado: {output_path}")
    return output_path


def save_interim(df: pd.DataFrame, filename: str) -> Path:
    """
    Guarda un dataset intermedio en data/interim/.

    Args:
        df: DataFrame a guardar.
        filename: Nombre del archivo de salida.

    Returns:
        Path del archivo guardado.
    """
    output_path = data_interim_dir(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Dataset intermedio guardado: {output_path}")
    return output_path
