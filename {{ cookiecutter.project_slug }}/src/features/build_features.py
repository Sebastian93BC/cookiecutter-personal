import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import scipy.stats as stats
from rapidfuzz import fuzz
from IPython.display import display
from scipy.stats import skew, kurtosis
import unicodedata
from difflib import SequenceMatcher
from itertools import combinations
from category_encoders import TargetEncoder
from sklearn.preprocessing import KBinsDiscretizer


# Estadísticas descriptivas detalladas para columnas cuantitativas y cualitativas

def describe_dataset(df):
    """
    Generates a detailed description of each column in a DataFrame,
    including centrality, dispersion, and shape statistics.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.

    Returns
    -------
    summary : dict
        Dictionary with 'quantitative' and 'qualitative' descriptions.
    """
    summary = {}

    # --- Quantitative columns ---
    quant_cols = df.select_dtypes(include=['int64', 'float64']).columns
    quant_summary = pd.DataFrame(index=quant_cols, columns=[
        'count', 'mean', 'median', 'mode', 'min', 'max', 'range',
        'variance', 'std_dev', 'skewness', 'kurtosis'
    ])

    for col in quant_cols:
        data = df[col].dropna()
        quant_summary.loc[col, 'count'] = data.count()
        quant_summary.loc[col, 'mean'] = data.mean()
        quant_summary.loc[col, 'median'] = data.median()
        quant_summary.loc[col, 'mode'] = data.mode().iloc[0] if not data.mode().empty else None
        quant_summary.loc[col, 'min'] = data.min()
        quant_summary.loc[col, 'max'] = data.max()
        quant_summary.loc[col, 'range'] = data.max() - data.min()
        quant_summary.loc[col, 'variance'] = data.var()
        quant_summary.loc[col, 'std_dev'] = data.std()
        quant_summary.loc[col, 'skewness'] = skew(data)
        quant_summary.loc[col, 'kurtosis'] = kurtosis(data)

    summary['quantitative'] = quant_summary

    # --- Qualitative columns ---
    qual_cols = df.select_dtypes(include=['object']).columns
    qual_summary = {}
    for col in qual_cols:
        data = df[col].dropna()
        freq = data.value_counts()
        prop = data.value_counts(normalize=True)
        qual_summary[col] = pd.DataFrame({'count': freq, 'proportion': prop})

    summary['qualitative'] = qual_summary

    return summary

# Evaluación de normalidad para variables numéricas
def check_normality(df):
    """
    Evalúa la normalidad de las variables numéricas de un DataFrame usando:
    - Test estadístico de Shapiro-Wilk
    - Asimetría (Skewness)
    - Curtosis (Kurtosis)
    - Visualizaciones: Histograma + KDE y Q-Q Plot

    Retorna un DataFrame resumen con los resultados.
    """

    # 1️⃣ Seleccionar únicamente columnas numéricas
    # (int y float), ya que la normalidad solo aplica a variables cuantitativas
    cols = df.select_dtypes(include=[np.number]).columns
    results = []

    # 2️⃣ Configuración de la grilla de gráficos
    # Cada variable tendrá:
    # - Columna 1: Histograma + KDE
    # - Columna 2: Q-Q Plot
    fig, axes = plt.subplots(len(cols), 2, figsize=(12, 4 * len(cols)))

    # Ajuste especial cuando solo hay una variable
    # (matplotlib devuelve un array 1D en lugar de 2D)
    if len(cols) == 1:
        axes = np.expand_dims(axes, axis=0)

    # 3️⃣ Iterar por cada columna numérica
    for i, col in enumerate(cols):
        
        # Eliminar valores nulos para evitar errores en los tests
        data = df[col].dropna()
        
        # =============================
        # TESTS DE NORMALIDAD
        # =============================

        # 4️⃣ Test de Shapiro-Wilk
        # - H0: los datos siguen una distribución normal
        # - p-value > 0.05 → NO se rechaza la normalidad
        # Ideal para muestras pequeñas y medianas (n < 5000)
        stat, p_value = stats.shapiro(data)
        
        # 5️⃣ Medidas de forma
        # Asimetría:
        #   ≈ 0  → distribución simétrica
        #   > 0  → sesgo a la derecha
        #   < 0  → sesgo a la izquierda
        skew = data.skew()
        
        # Curtosis (pandas devuelve curtosis "excesiva"):
        #   ≈ 0  → similar a normal
        #   > 0  → más picuda (leptocúrtica)
        #   < 0  → más plana (platicúrtica)
        kurt = data.kurtosis()
        
        # 6️⃣ Guardar resultados en una lista de diccionarios
        results.append({
            'Columna': col,
            'p-value (Shapiro)': round(p_value, 4),
            'Asimetría': round(skew, 2),
            'Curtosis': round(kurt, 2),
            '¿Es Normal? (p > 0.05)': p_value > 0.05
        })

        # =============================
        # VISUALIZACIONES
        # =============================

        # 7️⃣ Histograma con KDE
        # Permite observar la forma de la distribución
        sns.histplot(data, kde=True, ax=axes[i, 0], color='skyblue')
        axes[i, 0].set_title(f'Distribución: {col}')
        
        # 8️⃣ Q-Q Plot
        # Si los puntos siguen la línea roja,
        # los datos se aproximan a una distribución normal
        stats.probplot(data, dist="norm", plot=axes[i, 1])
        axes[i, 1].set_title(f'Q-Q Plot: {col}')

    # Ajustar espacios entre gráficos
    fig.tight_layout()

    # 9️⃣ Retornar resultados como DataFrame
    return pd.DataFrame(results), fig


# identificación de valores nulos/faltantes y eliminación de columnas con alto porcentaje de nulos
def plot_missing_values_heatmap(
    df,
    figsize=(14, 6),
    cmap='viridis',
    title='Heatmap de valores faltantes en el dataset',
    xlabel='Variables',
    ylabel='Observaciones',
    show=True
):
    """
    Grafica un heatmap de valores faltantes en un DataFrame
    e indica qué representa cada color.
    """

    plt.figure(figsize=figsize)

    ax = sns.heatmap(
        df.isnull(),
        cbar=True,
        yticklabels=False,
        cmap=cmap
    )

    # Personalizar la barra de color
    cbar = ax.collections[0].colorbar
    cbar.set_ticks([0, 1])
    cbar.set_ticklabels(['Dato presente', 'Dato faltante'])
    cbar.set_label('Estado del dato', rotation=270, labelpad=20)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if show:
        plt.show()


def missing_values_by_column(
    df,
    sort=True,
    ascending=False,
    round_decimals=4
):
    """
    Generates a summary table of missing values by column.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to analyze.
    sort : bool, optional
        Sort by missing value proportion.
    ascending : bool, optional
        Sort order for the proportion column.
    round_decimals : int, optional
        Number of decimals for the proportion column.

    Returns
    -------
    pandas.DataFrame
        Summary table with missing count and proportion per column.
    """

    # Count of missing values per column
    missing_count = df.isnull().sum()

    # Proportion of missing values per column
    missing_ratio = df.isnull().mean().round(round_decimals)

    # Summary table
    missing_by_column = (
        pd.DataFrame({
            'missing_count': missing_count,
            'missing_ratio': missing_ratio
        })
    )

    if sort:
        missing_by_column = missing_by_column.sort_values(
            by='missing_ratio',
            ascending=ascending
        )

    return missing_by_column


def drop_high_null_columns(df, threshold=0.8, verbose=True):
    """
    Drops columns from a DataFrame that have a proportion of missing values 
    above a specified threshold and provides a summary of dropped columns.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to process.
    threshold : float, optional (default=0.8)
        Maximum allowed proportion of missing values per column. Columns with a 
        higher proportion will be dropped.
    verbose : bool, optional (default=True)
        If True, prints a summary of the columns dropped and the reason.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns exceeding the missing value threshold removed.
    dict
        A summary dictionary containing the dropped columns and the reason.
    """

    # Calculate missing value ratio for each column
    missing_ratio = df.isnull().mean()

    # Identify columns to drop
    cols_to_drop = missing_ratio[missing_ratio > threshold].index.tolist()

    # Create a summary of dropped columns
    dropped_summary = {
        'dropped_columns': cols_to_drop,
        'reason': f'Missing value proportion greater than {threshold}'
    }

    # Optionally print summary
    if verbose:
        if cols_to_drop:
            print("Columns dropped due to high missing values:")
            for col in cols_to_drop:
                print(f"- {col} ({missing_ratio[col]:.2f} missing)")
        else:
            print("No columns were dropped. All columns are below the threshold.")

    # Drop the columns and return
    df_cleaned = df.drop(columns=cols_to_drop)

    # return df_cleaned, dropped_summary
    return df_cleaned


def drop_rows_high_nulls(df, threshold=0.5):
    """
    Drop rows from a DataFrame that have a proportion of missing values
    higher than the specified threshold.

    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame to clean.
    threshold : float, optional (default=0.5)
        The maximum allowed proportion of missing values per row.
        Rows with a higher proportion will be dropped.

    Returns:
    --------
    pd.DataFrame
        A new DataFrame with rows containing too many missing values removed.
    pd.DataFrame
        A summary DataFrame showing dropped rows and their null proportion.
    """

    # Calculate the proportion of nulls per row
    null_proportion = df.isnull().mean(axis=1)

    # Identify rows to drop
    rows_to_drop = null_proportion[null_proportion > threshold]

    # Drop rows exceeding the threshold
    df_cleaned = df.drop(rows_to_drop.index)

    # Create a summary of dropped rows
    dropped_summary = pd.DataFrame({
        'row_index': rows_to_drop.index,
        'null_proportion': rows_to_drop.values
    })

    print(f"Dropped {len(rows_to_drop)} rows out of {df.shape[0]} "
          f"({len(rows_to_drop)/df.shape[0]*100:.2f}%) due to high null values.")

    return df_cleaned


def show_duplicate_records(df, subset=None, keep=False, sort=True, verbose=True):
    """
    Identifies and displays duplicate rows in a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to analyze for duplicates.
    subset : list or None, optional (default=None)
        Columns to consider when identifying duplicates. If None, all columns are used.
    keep : {'first', 'last', False}, optional (default=False)
        Determines which duplicates to mark:
        - 'first' : mark duplicates except the first occurrence
        - 'last' : mark duplicates except the last occurrence
        - False : mark all duplicates
    sort : bool, optional (default=True)
        If True, sort the duplicate rows by all columns.
    verbose : bool, optional (default=True)
        If True, prints the number of duplicates found.

    Returns
    -------
    pd.DataFrame
        DataFrame containing all duplicate rows based on the criteria.
    """

    # Identify duplicate rows
    duplicates = df[df.duplicated(subset=subset, keep=keep)]

    # Optionally print number of duplicates
    if verbose:
        print(f"Found {duplicates.shape[0]} duplicate records:")

    # Optionally sort duplicates by all columns
    if sort and not duplicates.empty:
        duplicates = duplicates.sort_values(by=duplicates.columns.tolist())
        if verbose:
            print("DataFrame sorted by all columns:")

    # Display the duplicates (useful in Jupyter/Colab)
    if not duplicates.empty:
        display(duplicates)
    else:
        if verbose:
            print("No duplicate records found.")

    return duplicates



def check_and_drop_duplicates(df, subset=None, keep='first', verbose=True):
    """
    Checks for duplicate rows in a DataFrame and drops them.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to analyze.
    subset : list or None, optional (default=None)
        Columns to consider when identifying duplicates. If None, all columns are used.
    keep : {'first', 'last', False}, optional (default='first')
        Determines which duplicates to keep:
        - 'first' : keep first occurrence
        - 'last' : keep last occurrence
        - False : drop all duplicates
    verbose : bool, optional (default=True)
        If True, prints a summary of duplicate records found and removed.

    Returns
    -------
    df_cleaned : pandas.DataFrame
        DataFrame with duplicates removed according to parameters.
    summary : dict
        Summary dictionary containing number of duplicates removed and columns considered.
    """

    if subset is None:
        subset = df.columns.tolist()
    
    # Contar duplicados antes de eliminar
    num_duplicates = df.duplicated(subset=subset, keep=keep).sum()

    # Eliminar duplicados
    df_cleaned = df.drop_duplicates(subset=subset, keep=keep)

    # Crear resumen
    summary = {
        'subset_columns': subset,
        'duplicates_removed': int(num_duplicates)
    }

    if verbose:
        if num_duplicates > 0:
            print(f"Columns evaluated: {subset}")
            print(f"Duplicate rows removed: {num_duplicates}")
        else:
            print("No duplicate rows found.")

    return df_cleaned


# Detección de outliers usando el método de Tukey (IQR)
def detect_outliers_iqr(
    df,
    cols=None,
    iqr_factor=1.5,
    show_plots=True
):
    """
    Detecta outliers usando el método de Tukey (IQR).

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame de entrada.
    cols : list, opcional
        Columnas numéricas a analizar. Si es None, se usan todas las numéricas.
    iqr_factor : float, default=1.5
        Factor multiplicativo del IQR (1.5 = Tukey clásico).
    show_plots : bool, default=True
        Si True, muestra boxplots por variable.

    Retorna
    -------
    summary_df : pd.DataFrame
        Resumen con límites, cantidad y porcentaje de outliers por variable.
    outliers_dict : dict
        Diccionario con índices de outliers por variable.
    """

    # 1️⃣ Selección de columnas numéricas
    if cols is None:
        cols = df.select_dtypes(include='number').columns

    summary = []
    outliers_dict = {}

    # 2️⃣ Configuración de gráficos
    if show_plots:
        fig, axes = plt.subplots(len(cols), 1, figsize=(8, 4 * len(cols)))
        if len(cols) == 1:
            axes = [axes]

    # 3️⃣ Iteración por columna
    for i, col in enumerate(cols):
        data = df[col].dropna()

        # Cuartiles
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1

        # Límites de Tukey
        lower_bound = Q1 - iqr_factor * IQR
        upper_bound = Q3 + iqr_factor * IQR

        # Identificación de outliers
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outliers_dict[col] = outliers.index.tolist()

        # Resumen estadístico
        summary.append({
            'Columna': col,
            'Q1': round(Q1, 2),
            'Q3': round(Q3, 2),
            'IQR': round(IQR, 2),
            'Límite Inferior': round(lower_bound, 2),
            'Límite Superior': round(upper_bound, 2),
            'Outliers (#)': len(outliers),
            'Outliers (%)': round(len(outliers) / len(df) * 100, 2)
        })

        # 4️⃣ Boxplot
        if show_plots:
            sns.boxplot(x=data, ax=axes[i], color='skyblue')
            axes[i].set_title(f'Boxplot - {col}')

    if show_plots:
        fig.tight_layout()

    return pd.DataFrame(summary), outliers_dict, (fig if show_plots else None)


# Z-scores para detección de valores extremos
def compute_z_scores(
    df,
    cols=None,
    threshold=3.0,
    return_outliers=True
):
    """
    Calculates Z-scores to measure deviations from the mean.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    cols : list or None, optional (default=None)
        Numerical columns to evaluate. If None, all numerical columns are used.
    threshold : float, optional (default=3.0)
        Absolute Z-score value above which a data point is considered an outlier.
    return_outliers : bool, optional (default=True)
        If True, returns indices of rows exceeding the Z-score threshold.

    Returns
    -------
    z_scores_df : pandas.DataFrame
        DataFrame containing Z-scores for each selected column.
    summary_df : pandas.DataFrame
        Summary with mean, std, and number of extreme values per column.
    outliers_dict : dict (optional)
        Dictionary with indices of rows where |Z| > threshold per column.
    """

    # 1️⃣ Select numerical columns
    if cols is None:
        cols = df.select_dtypes(include='number').columns

    z_scores_df = pd.DataFrame(index=df.index)
    summary = []
    outliers_dict = {}

    # 2️⃣ Compute Z-scores per column
    for col in cols:
        data = df[col]

        mean = data.mean()
        std = data.std()

        # Avoid division by zero
        if std == 0 or pd.isna(std):
            z_scores = pd.Series(0, index=df.index)
        else:
            z_scores = (data - mean) / std

        z_scores_df[f'Z_{col}'] = z_scores

        # Identify extreme values
        extreme_mask = z_scores.abs() > threshold
        outliers_dict[col] = df.loc[extreme_mask].index.tolist()

        summary.append({
            'Columna': col,
            'Media': round(mean, 2),
            'Desviación estándar': round(std, 2),
            'Umbral |Z|': threshold,
            'Valores extremos (#)': int(extreme_mask.sum()),
            'Valores extremos (%)': round(extreme_mask.mean() * 100, 2)
        })

    if return_outliers:
        return z_scores_df, pd.DataFrame(summary), outliers_dict

    return z_scores_df, pd.DataFrame(summary)



# Function to find out-of-range row indices
def get_out_of_range_indices(df, column, min_value=None, max_value=None):
    """
    Identifies row indices where values in a given column
    fall outside a specified range.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    column : str
        Column name to evaluate.
    min_value : float or int or None, optional (default=None)
        Minimum allowed value (inclusive).
        If None, no lower bound is applied.
    max_value : float or int or None, optional (default=None)
        Maximum allowed value (inclusive).
        If None, no upper bound is applied.

    Returns
    -------
    out_of_range_indices : pandas.Index
        Index of rows with values outside the specified range.

    Notes
    -----
    - NaN values are ignored.
    - The function does NOT modify the original DataFrame.
    """

    # Ensure the column exists
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")

    # Drop NaN values to avoid false positives
    data = df[column].dropna()

    # Initialize boolean mask as all False
    mask = pd.Series(False, index=data.index)

    # Apply lower bound condition if provided
    if min_value is not None:
        mask |= data < min_value

    # Apply upper bound condition if provided
    if max_value is not None:
        mask |= data > max_value

    # Return indices where condition is True
    return mask[mask].index


# Function to drop rows using a list of indices

def drop_rows_by_indices(df, indices, reset_index=False):
    """
    Removes rows from a DataFrame using a given list of indices.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    indices : list or pandas.Index
        Row indices to remove.
    reset_index : bool, optional (default=False)
        If True, resets the DataFrame index after dropping rows.

    Returns
    -------
    df_cleaned : pandas.DataFrame
        DataFrame with specified rows removed.

    Notes
    -----
    - The original DataFrame is NOT modified.
    - Indices not found in the DataFrame are safely ignored.
    """

    # Drop rows by index
    df_cleaned = df.drop(index=indices, errors='ignore')

    # Optionally reset index
    if reset_index:
        df_cleaned = df_cleaned.reset_index(drop=True)

    return df_cleaned




## transformaciones de variables

def sqrt_transform_feature(
    df,
    column,
    new_column_name=None,
    drop_original=False
):
    """
    Applies a square root transformation to a numerical feature
    and creates a new column.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    column : str
        Column to transform.
    new_column_name : str or None, optional (default=None)
        Name of the transformed column.
        If None, '<column>_sqrt' is used.
    drop_original : bool, optional (default=False)
        If True, drops the original column after transformation.

    Returns
    -------
    df_transformed : pandas.DataFrame
        DataFrame including the square-root-transformed feature.

    Notes
    -----
    - Values must be >= 0. Negative values are converted to NaN.
    - The square root transformation reduces right skewness.
    - The original DataFrame is NOT modified.
    """

    # Copy DataFrame to avoid in-place modification
    df_transformed = df.copy()

    # Define new column name
    if new_column_name is None:
        new_column_name = f"{column}_sqrt"

    # Ensure numeric values
    values = pd.to_numeric(df_transformed[column], errors='coerce')

    # Replace negative values with NaN
    values = values.where(values >= 0)

    # Apply square root transformation
    df_transformed[new_column_name] = np.sqrt(values)

    # Optionally drop original column
    if drop_original:
        df_transformed = df_transformed.drop(columns=[column])

    return df_transformed



def log_transform_feature(
    df,
    column,
    new_column_name=None,
    drop_original=False,
    use_log1p=True
):
    """
    Applies a logarithmic transformation to a target variable.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    column : str
        Target column to transform.
    new_column_name : str or None, optional (default=None)
        Name of the transformed column.
        If None, '<target_column>_log' is used.
    drop_original : bool, optional (default=False)
        If True, drops the original target column.
    use_log1p : bool, optional (default=True)
        If True, applies log(1 + x) to safely handle zero values.
        If False, applies natural log (ln).

    Returns
    -------
    df_transformed : pandas.DataFrame
        DataFrame including the log-transformed target.

    Notes
    -----
    - log1p is recommended when the target contains zeros.
    - Negative values will result in NaN.
    - The original DataFrame is NOT modified.
    """

    # Copy DataFrame to avoid in-place modification
    df_transformed = df.copy()

    # Define new column name
    if new_column_name is None:
        suffix = 'log1p' if use_log1p else 'log'
        new_column_name = f"{column}_{suffix}"

    # Ensure numeric values
    target_values = pd.to_numeric(df_transformed[column], errors='coerce')

    # Apply log transformation
    if use_log1p:
        df_transformed[new_column_name] = np.log1p(target_values)
    else:
        df_transformed[new_column_name] = np.log(target_values)

    # Optionally drop original target column
    if drop_original:
        df_transformed = df_transformed.drop(columns=[column])

    return df_transformed


# procesamiento de variables categóricas

def standardize_categorical_columns(df, columns):
    """
    Standardizes categorical text columns by:
    - Converting text to lowercase
    - Removing leading/trailing and extra internal spaces
    - Normalizing accents (e.g., á → a, ñ → n)

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    columns : list
        List of categorical column names to standardize.

    Returns
    -------
    df_cleaned : pandas.DataFrame
        DataFrame with standardized categorical columns.

    Notes
    -----
    - NaN values are preserved.
    - The original DataFrame is NOT modified.
    - Accent normalization is useful for consistent encoding.
    """

    def normalize_text(text):
        """
        Helper function to normalize a single text value.
        """
        if pd.isna(text):
            return text

        # Convert to string and lowercase
        text = str(text).lower()

        # Remove leading/trailing spaces and normalize internal spaces
        text = " ".join(text.split())

        # Normalize accents (unicode normalization)
        text = unicodedata.normalize('NFKD', text)
        text = ''.join(char for char in text if not unicodedata.combining(char))

        return text

    # Copy DataFrame to avoid in-place modification
    df_cleaned = df.copy()

    # Apply normalization to each specified column
    for col in columns:
        if col not in df_cleaned.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame.")

        df_cleaned[col] = df_cleaned[col].apply(normalize_text)

    return df_cleaned




def normalize_similar_values(
    df,
    column,
    similarity_threshold=0.95
):
    """
    Identifies highly similar values in a categorical column and creates
    a new normalized column where similar values are standardized.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    column : str
        Column to normalize.
    similarity_threshold : float (0–1)
        Minimum similarity score to consider values equivalent.

    Returns
    -------
    df_out : pandas.DataFrame
        DataFrame with a new column: <column>_normalized
    groups : list of dict
        Detected similarity groups and chosen canonical values.
    """

    # Unique non-null values
    values = (
        df[column]
        .dropna()
        .astype(str)
        .str.strip()
        .str.lower()
        .unique()
        .tolist()
    )

    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()

    # --- Step 1: Build similarity graph ---
    graph = {v: set() for v in values}

    for v1, v2 in combinations(values, 2):
        if similarity(v1, v2) >= similarity_threshold:
            graph[v1].add(v2)
            graph[v2].add(v1)

    # --- Step 2: Extract connected components ---
    visited = set()
    groups = []

    for value in graph:
        if value not in visited:
            stack = [value]
            component = set()

            while stack:
                v = stack.pop()
                if v not in visited:
                    visited.add(v)
                    component.add(v)
                    stack.extend(graph[v])

            groups.append(component)

    # --- Step 3: Choose canonical value (most frequent) ---
    value_counts = df[column].str.lower().value_counts()

    mapping = {}
    group_info = []

    for group in groups:
        canonical = max(group, key=lambda x: value_counts.get(x, 0))
        for v in group:
            mapping[v] = canonical

        group_info.append({
            "canonical_value": canonical,
            "group_members": sorted(group)
        })

    # --- Step 4: Create normalized column ---
    df_out = df.copy()
    df_out[f"{column}_normalized"] = (
        df_out[column]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(mapping)
    )

    return df_out, group_info



def group_low_frequency_categories(
    df,
    columns,
    threshold_pct=0.005,
    threshold_abs=None,
    new_category_name="otros"
):
    """
    Groups low frequency categories into a single category for categorical columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    columns : list of str
        List of categorical columns to process.
    threshold_pct : float, optional (default=0.005)
        Categories with relative frequency lower than this threshold will be grouped.
    threshold_abs : int, optional (default=None)
        Categories with absolute frequency lower than this threshold will be grouped.
        If provided, overrides threshold_pct.
    new_category_name : str, optional (default="otros")
        Name for the new grouped category.

    Returns
    -------
    df_out : pandas.DataFrame
        DataFrame with low-frequency categories grouped.
    grouped_info : dict
        Dictionary with column as key and list of grouped categories as value.
    """

    df_out = df.copy()
    grouped_info = {}

    for col in columns:
        value_counts = df_out[col].value_counts()
        total = len(df_out)

        # Determine threshold
        if threshold_abs is not None:
            low_freq_values = value_counts[value_counts < threshold_abs].index.tolist()
        else:
            low_freq_values = value_counts[value_counts / total < threshold_pct].index.tolist()

        # Replace low frequency values
        df_out[col] = df_out[col].apply(lambda x: new_category_name if x in low_freq_values else x)

        grouped_info[col] = low_freq_values

    return df_out, grouped_info


#


def add_age_from_year(
    df,
    year_column='year',
    reference_year=None,
    new_column_name='age',
    drop_original=False
):
    """
    Adds age from a given reference year.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    year_column : str, optional (default='year')
        Column containing the year.
    reference_year : int or None, optional (default=None)
        Reference year used to calculate age.
        If None, the current year is used.
    new_column_name : str, optional (default='Edad')
        Name of the new age column.
    drop_original : bool, optional (default=False)
        If True, drops the original year column after creating the age column.

    Returns
    -------
    df_with_age : pandas.DataFrame
        DataFrame including the new age column.

    Notes
    -----
    - Negative ages (future years) are clipped to 0.
    - Missing or invalid year values are preserved as NaN.
    - The original DataFrame is NOT modified.
    """

    # Copy DataFrame to avoid in-place modification
    df_with_age = df.copy()

    # Determine reference year
    if reference_year is None:
        reference_year = pd.Timestamp.now().year

    # Ensure year column is numeric
    year_values = pd.to_numeric(df_with_age[year_column], errors='coerce')

    # Calculate age
    df_with_age[new_column_name] = reference_year - year_values

    # Clip negative ages (e.g., future vehicle years)
    df_with_age[new_column_name] = df_with_age[new_column_name].clip(lower=0)

    # Optionally drop original year column
    if drop_original:
        df_with_age = df_with_age.drop(columns=[year_column])

    return df_with_age


#
def apply_onehot_encoding(
    df,
    low_freq_threshold_pct=0.01,
    onehot_columns=None,
    new_category_name="otros"
):
    """
    Preprocess categorical variables:
    1. Groups low-frequency categories into 'otros' (percentage-based)
    2. Applies One-Hot Encoding WITHOUT dropping original columns
    3. Returns processed DataFrame and info dictionaries
    """

    df_out = df.copy()
    grouped_categories = {}
    encoders = {}

    # --- Step 1: Group low-frequency categories ---
    categorical_cols = df_out.select_dtypes(include=["object", "category"]).columns.tolist()

    for col in categorical_cols:
        value_counts = df_out[col].value_counts(normalize=True)
        low_freq_values = value_counts[value_counts < low_freq_threshold_pct].index.tolist()

        if low_freq_values:
            df_out[col] = df_out[col].where(
                ~df_out[col].isin(low_freq_values),
                new_category_name
            )

        grouped_categories[col] = low_freq_values

    # --- Step 2: One-Hot Encoding (WITHOUT dropping originals) ---
    if onehot_columns is not None:
        for col in onehot_columns:
            dummies = pd.get_dummies(
                df_out[col],
                prefix=col,
                drop_first=True
            )
            df_out = pd.concat([df_out, dummies], axis=1)

    return df_out, grouped_categories

#

def apply_target_encoding(
    df,
    categorical_column,
    target_column,
    smoothing=0.3
):
    """
    Applies target encoding to a high-cardinality categorical column.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    categorical_column : str
        Name of the categorical column to encode.
    target_column : str
        Name of the target variable (e.g., Precio).
    smoothing : float, optional (default=0.3)
        Smoothing factor to balance category mean with global mean.
        Higher values -> more shrinkage to global mean.

    Returns
    -------
    df_out : pandas.DataFrame
        DataFrame with a new column <categorical_column>_te containing
        the target-encoded values.
    encoder : category_encoders.TargetEncoder
        Fitted encoder object (useful for production or new data).
    """

    df_out = df.copy()

    # Initialize the encoder
    encoder = TargetEncoder(
        cols=[categorical_column],
        smoothing=smoothing,
        drop_invariant=False
    )

    # Fit and transform
    df_out[categorical_column + "_te"] = encoder.fit_transform(
        df_out[categorical_column],
        df_out[target_column]
    )[categorical_column]

    return df_out, encoder


#

def apply_bin_encoding(
    dataframe: pd.DataFrame,
    target_column: str,
    bins_per_column: dict,
    strategy: str = 'uniform'
) -> pd.DataFrame:
    """
    Applies Bin Encoding to high-cardinality categorical columns in a pandas DataFrame,
    using the columns and bins specified in the `bins_per_column` dictionary.

    Parameters:
    -----------
    dataframe : pd.DataFrame
        Input DataFrame containing the data.
    target_column : str
        Name of the target column (e.g., 'Precio').
    bins_per_column : dict
        Dictionary with column names as keys and number of bins as values (e.g., {'Marca': 5, 'Modelo': 10}).
    strategy : str, optional (default='uniform')
        Strategy for KBinsDiscretizer ('uniform', 'quantile', or 'kmeans').

    Returns:
    --------
    pd.DataFrame
        DataFrame with original columns preserved and new bin-encoded columns added.
    """
    # Create a copy of the original DataFrame
    df_transformed = dataframe.copy()

    for column, bins in bins_per_column.items():
        # Initialize the KBinsDiscretizer with the specific bins for this column
        discretizer = KBinsDiscretizer(n_bins=bins, encode='ordinal', strategy=strategy)

        # Create a temporary DataFrame grouping by the categorical column and the target
        temp_df = df_transformed[[column, target_column]].dropna()

        # Group by the categorical column and calculate the mean of the target
        grouped = temp_df.groupby(column)[target_column].mean().reset_index()

        # Apply KBinsDiscretizer to the target means
        encoded_bins = discretizer.fit_transform(grouped[[target_column]])

        # Map the original categories to their bin-encoded values
        bin_mapping = dict(zip(grouped[column], encoded_bins.flatten()))

        # Create a new column with the '_bin_encoding' suffix
        new_column_name = f"{column}_bin_encoding"
        df_transformed[new_column_name] = df_transformed[column].map(bin_mapping)

    return df_transformed


#