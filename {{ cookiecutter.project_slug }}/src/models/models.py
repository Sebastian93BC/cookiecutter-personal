import numpy as np

from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV

from src.utils.general_functions import Utils


class Models:
    """
    A class that manages machine learning models and performs hyperparameter
    tuning using GridSearchCV.
    """

    def __init__(self):
        """
        Initializes the Models class with a set of regression models
        and their corresponding hyperparameter grids.
        """
        self.reg = {
            'SVR': SVR(),
            'GRADIENT': GradientBoostingRegressor()
        }

        self.param = {
            'SVR': {
                'C': [1, 5, 10],
                'gamma': ['scale', 'auto'],
                'kernel': ['linear', 'poly', 'rbf']
            },
            'GRADIENT': {
                'loss': ['squared_error', 'absolute_error'],
                'learning_rate': [0.01, 0.05, 0.1],
            }
        }

    def grid_training(self, X, y):
        """
        Performs hyperparameter optimization using GridSearchCV for all
        registered models and exports the best performing one.

        Args:
            X (pd.DataFrame): Training features.
            y (pd.Series or pd.DataFrame): Target variable.
        """

        best_score = 999
        best_model = None

        for name, reg in self.reg.items():
            grid_reg = GridSearchCV(reg, self.param[name], cv=3)
            grid_reg.fit(X, y.values.ravel())
            score = np.abs(grid_reg.best_score_)

            if score < best_score:
                best_score = score
                best_model = grid_reg.best_estimator_
                print(f'New best score: {best_score} found with model: {name}')
        
        utils = Utils()
        utils.model_export(best_model, best_score)
