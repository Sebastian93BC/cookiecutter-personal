import pandas as pd
import itertools
from rapidfuzz import fuzz
from statsmodels.stats.outliers_influence import variance_inflation_factor
from matplotlib import pyplot as plt
import seaborn as sns
import scipy.stats as stats
from itertools import combinations

#
def count_unique_cases_by_categorical_column(df):
    """
    Returns the number of unique values in each categorical column.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with two columns:
        - 'column': column name
        - 'unique_count': number of unique values in that column
    """

    # Select categorical columns (object or category dtype)
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns

    # Build results as a list of dicts
    results = [
        {"column": col, "unique_count": df[col].nunique(dropna=True)}
        for col in categorical_cols
    ]

    return pd.DataFrame(results)

#
def find_high_similarity_pairs(
    df,
    column,
    similarity_threshold=0.9
):
    """
    Finds pairs of categorical values within a column
    that have high textual similarity.

    Diagnostic-only function.
    No automatic corrections are applied.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    column : str
        Name of the categorical column to analyze.
    similarity_threshold : int, optional
        Minimum similarity score (0-1) to consider a pair related.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing pairs of similar values and their similarity score.
        Returns an empty DataFrame if no pairs meet the threshold.
    """

    similarity_threshold  = similarity_threshold * 100
    unique_values = (
        df[column]
        .dropna()
        .astype(str)
        .unique()
    )

    results = []

    for val1, val2 in itertools.combinations(unique_values, 2):
        score = fuzz.ratio(val1, val2)

        if score >= similarity_threshold:
            results.append({
                "value_1": val1,
                "value_2": val2,
                "similarity_score": score
            })

    # Always return a DataFrame with expected columns
    results_df = pd.DataFrame(
        results,
        columns=["value_1", "value_2", "similarity_score"]
    )

    if not results_df.empty:
        results_df = results_df.sort_values(
            by="similarity_score",
            ascending=False
        )

    return results_df

#
def calculate_vif(df, features):
    """
    Calculates Variance Inflation Factor (VIF) for a set of predictors.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    features : list
        List of numerical feature names to evaluate.

    Returns
    -------
    vif_df : pandas.DataFrame
        DataFrame with VIF values per feature.

    Notes
    -----
    - VIF > 5 indicates moderate multicollinearity.
    - VIF > 10 indicates severe multicollinearity.
    - Features must be numerical and contain no NaN values.
    """

    # Subset and drop missing values
    X = df[features].dropna()

    # Add constant manually for statsmodels
    X = X.assign(constant=1)

    vif_data = []

    for i, col in enumerate(X.columns[:-1]):  # exclude constant
        vif_data.append({
            'Feature': col,
            'VIF': round(
                variance_inflation_factor(X.values, i),
                2
            )
        })

    return pd.DataFrame(vif_data)

#
def residuals_diagnostic_plot(
    model,
    X,
    y,
    lowess=True
):
    """
    Generates a residuals vs fitted values diagnostic plot
    to assess linear model assumptions.

    Parameters
    ----------
    model : fitted regression model
        Trained regression model with a predict() method.
    X : pandas.DataFrame or array-like
        Feature matrix used for prediction.
    y : pandas.Series or array-like
        True target values (transformed scale).
    lowess : bool, optional (default=True)
        If True, overlays a LOWESS smooth curve to highlight patterns.

    Returns
    -------
    residuals_df : pandas.DataFrame
        DataFrame containing fitted values and residuals.

    Notes
    -----
    - Random scatter around zero indicates a well-specified linear model.
    - Patterns, curves or funnels indicate misspecification or heteroscedasticity.
    """

    # Predict fitted values
    y_pred = model.predict(X)

    # Compute residuals
    residuals = y - y_pred

    # Build DataFrame for inspection
    residuals_df = pd.DataFrame({
        'Fitted values': y_pred,
        'Residuals': residuals
    })

    # Plot
    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        x='Fitted values',
        y='Residuals',
        data=residuals_df,
        alpha=0.5
    )

    # Reference line at zero
    plt.axhline(0, linestyle='--', color='red')

    # Optional LOWESS smoothing line
    if lowess:
        sns.regplot(
            x='Fitted values',
            y='Residuals',
            data=residuals_df,
            scatter=False,
            lowess=True,
            line_kws={'color': 'black'}
        )

    plt.title('Residuals vs Fitted Values')
    plt.xlabel('Fitted Values')
    plt.ylabel('Residuals')
    plt.show()

    return residuals_df

#
def count_out_of_range(df, columna, rango):
    """
    Cuenta la cantidad de elementos en una columna de un DataFrame que están fuera de un rango dado.

    Args:
        df (pd.DataFrame): El DataFrame a analizar.
        columna (str): El nombre de la columna a evaluar.
        rango (tuple): Un rango (min, max) que define los límites.

    Returns:
        int: Cantidad de elementos fuera del rango.
    """
    min_val, max_val = rango
    fuera_de_rango = df[(df[columna] < min_val) | (df[columna] > max_val)]
    return len(fuera_de_rango)

#
def evaluate_categorical_relevance(df, target_column="Precio", categorical_columns=None):
    """
    Performs statistical relevance tests for categorical variables:
    1. ANOVA (categorical vs target)
    2. Chi-squared test for dependency between categorical variables
    
    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame
    target_column : str
        Continuous target variable (e.g., Precio)
    categorical_columns : list, optional
        List of categorical columns to evaluate. If None, detect automatically.

    Returns
    -------
    anova_results : pd.DataFrame
        DataFrame with ANOVA p-values per categorical variable
    chi2_matrix : pd.DataFrame
        DataFrame with Chi² p-values for each pair of categorical variables
    """
    
    df_eval = df.copy()
    
    if categorical_columns is None:
        categorical_columns = df_eval.select_dtypes(include=["object", "category"]).columns.tolist()
    
    # --- 1. ANOVA (categorical vs target) ---
    anova_list = []
    for col in categorical_columns:
        # Drop NaN in both target and predictor
        grouped_data = [df_eval[target_column][df_eval[col] == val] for val in df_eval[col].dropna().unique()]
        # Only perform ANOVA if more than 1 group
        if len(grouped_data) > 1:
            stat, p_value = stats.f_oneway(*grouped_data)
            anova_list.append({
                "variable": col,
                "anova_stat": round(stat, 4),
                "p_value": round(p_value, 4),
                "significant": p_value <= 0.05
            })
        else:
            anova_list.append({
                "variable": col,
                "anova_stat": None,
                "p_value": None,
                "significant": False
            })
    
    anova_results = pd.DataFrame(anova_list).sort_values("p_value")
    
    # --- 2. Chi² test between categorical variables ---
    chi2_dict = {}
    for col1, col2 in combinations(categorical_columns, 2):
        contingency_table = pd.crosstab(df_eval[col1], df_eval[col2])
        if contingency_table.size > 0:
            chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
            chi2_dict[(col1, col2)] = p
        else:
            chi2_dict[(col1, col2)] = None
    
    # Convert to symmetric matrix for readability
    chi2_matrix = pd.DataFrame(index=categorical_columns, columns=categorical_columns)
    for (col1, col2), p in chi2_dict.items():
        chi2_matrix.loc[col1, col2] = p
        chi2_matrix.loc[col2, col1] = p
    chi2_matrix.fillna(1, inplace=True)  # Diagonal = 1 (no self-dependency)
    
    return anova_results, chi2_matrix


# 