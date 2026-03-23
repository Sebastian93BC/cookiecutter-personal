import logging
import uuid
import joblib
from pathlib import Path
from typing import Tuple, Union, List

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor

from src.utils.paths import models_dir


class Utils:
    """
    Clase de utilidad que centraliza funciones para la manipulación de datos,
    preprocesamiento y gestión de modelos en flujos de trabajo de Machine Learning.
    """

    def load_dataset(self, path: Union[str, Path]) -> pd.DataFrame:
        """
        Carga un dataset desde un archivo CSV.
        """
        df = pd.read_csv(path)
        logging.info(f"Dataset cargado: {path}")
        return df

    def _get_models_dir(self) -> Path:
        """Obtiene y crea el directorio de modelos si no existe."""
        target = models_dir()
        target.mkdir(parents=True, exist_ok=True)
        return target

    def features_target(self, dataset: pd.DataFrame, drop_cols: Union[List[str], str], y: str) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Divide el dataset en características (X) y objetivo (y).
        """
        X = dataset.drop(drop_cols, axis=1)
        target = dataset[y]
        return X, target

    def split_data(self, X: pd.DataFrame, y: pd.Series, size: float = 0.3, seed: int = 42) -> Tuple:
        """
        Divide los datos en conjuntos de entrenamiento y prueba para evitar data leakage.
        """
        return train_test_split(X, y, test_size=size, random_state=seed)

    def model_export(self, clf, score: float):
        """
        Exporta el modelo entrenado a un archivo .pkl en una ruta dinámica.
        """
        target_dir = self._get_models_dir()
        unique_id = uuid.uuid4().hex
        file_path = target_dir / f"best_model_{unique_id}.pkl"

        print(f"Model Score: {score}")
        joblib.dump(clf, file_path)
        logging.info(f"Modelo exportado exitosamente en {file_path}")

    def process_and_scale_data(
        self, 
        X_train: pd.DataFrame, 
        X_test: pd.DataFrame, 
        scaler_name: str = "scaler_default.joblib"
    ) -> Tuple:
        """Ajusta un escalador a los datos de entrenamiento, lo guarda y transforma ambos conjuntos."""
        scaler_path = self._get_models_dir() / scaler_name
        scaler = StandardScaler()
        
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        joblib.dump(scaler, scaler_path)
        logging.info(f"Escalador guardado exitosamente en: {scaler_path}")
        return X_train_scaled, X_test_scaled

    def analyze_and_recommend_drops(
        self, 
        df: pd.DataFrame, 
        target_col: str, 
        correlation_threshold: float = 0.8, 
        importance_cutoff: float = 0.01
    ) -> Tuple[List[str], plt.Figure]:
        """
        Analiza el dataset para identificar variables redundantes o de bajo impacto predictivo.

        Combina un análisis de importancia de características mediante Random Forest con un 
        análisis de colinealidad. Si dos variables presentan una correlación superior al umbral, 
        se recomienda eliminar la de menor importancia. Adicionalmente, identifica variables 
        cuyo peso en el modelo es inferior al punto de corte establecido.

        Args:
            df (pd.DataFrame): DataFrame con las características y la variable objetivo.
            target_col (str): Nombre de la columna que actúa como variable dependiente.
            correlation_threshold (float): Límite de correlación de Pearson (0 a 1) para 
                detectar redundancia. Por defecto 0.8.
            importance_cutoff (float): Umbral mínimo de importancia relativa para conservar 
                una variable. Por defecto 0.01.

        Returns:
            Tuple[List[str], plt.Figure]: Lista de columnas sugeridas para eliminación y la figura generada.
        """


        # 1. Preparación de datos (Solo numéricos para evitar errores)
        X = df.drop(columns=[target_col]).select_dtypes(include=[np.number])
        y = df[target_col]
        
        # 2. Cálculo de Importancia (Random Forest)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        importance_dict = dict(zip(X.columns, model.feature_importances_))
        importances_df = pd.DataFrame({
            'Variable': X.columns,
            'Importancia': model.feature_importances_
        }).sort_values(by='Importancia', ascending=False)
    
        # 3. Análisis de Correlación
        corr_matrix = X.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        
        to_drop_corr = set()
        print(f"\n1. 🔄 Analizando redundancia (|r| > {correlation_threshold}):")
        for column in upper.columns:
            for index, row in upper[column].items():
                if row > correlation_threshold:
                    if importance_dict[column] < importance_dict[index]:
                        drop_candidate, keep_candidate = column, index
                    else:
                        drop_candidate, keep_candidate = index, column
                    
                    to_drop_corr.add(drop_candidate)
                    print(f"   • Conflicto: '{index}' y '{column}' (Corr: {row:.2f})")
                    print(f"     👉 Recomendación: Quitar '{drop_candidate}' por menor importancia.")
    
        # 4. Análisis de Bajo Valor
        print(f"\n2. 📉 Analizando bajo impacto (Aporte < {importance_cutoff}):")
        low_importance_vars = [v for v, imp in importance_dict.items() if imp < importance_cutoff and v not in to_drop_corr]
        for v in low_importance_vars:
            print(f"   • '{v}' aporta valor insignificante ({importance_dict[v]:.4f}).")
    
        # 5. Visualización
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            data=importances_df,
            x='Importancia',
            y='Variable',
            hue='Variable',
            palette='magma',
            legend=False,
            ax=ax
        )
        
        ax.axvline(importance_cutoff, color='red', linestyle='--', label='Umbral de corte')
        ax.set_title('Importancia Relativa de las Variables', fontsize=13)
        fig.tight_layout()
    
        total_to_drop = list(to_drop_corr) + low_importance_vars
        return total_to_drop, fig
