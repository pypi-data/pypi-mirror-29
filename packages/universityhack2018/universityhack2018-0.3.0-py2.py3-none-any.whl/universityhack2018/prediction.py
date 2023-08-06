import pandas as pd
import numpy as np
from universityhack2018.feature_engineering import FeatureEngineering
from universityhack2018.config import *
import pickle
import os

class Model:
    model_ = None
    clients_ = None

    def __init__(self, clients):
        if not isinstance(clients, pd.DataFrame) and not isinstance(clients, pd.Series):
            raise ValueError("The client object must be a pandas DataFrame or Series.")

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'objects/model.pkl'), 'rb') as input:
            self.model_ = pickle.load(input)

        self.clients_ = pd.DataFrame({key: pd.Series(clients[key], dtype=value) for (key, value) in DATA_TYPES.items()})

    def predict(self, as_df=False):
        fe = FeatureEngineering(self.clients_)

        self.clients_ = fe.polynomial_features()
        self.clients_ = fe.low_skewness()
        self.clients_ = fe.get_dummies()
        self.clients_ = fe.agg_num_feats()
        self.clients_ = fe.fill_na()
        self.clients_ = fe.scale()

        id_customer = self.clients_['ID_Customer']
        self.clients_ = self.clients_.drop(REMOVE, axis=1)
        self.clients_.replace([np.inf, -np.inf], np.nan)
        self.clients_ = self.clients_.fillna(0)
        predictions = self.model_.predict(self.clients_.drop('ID_Customer', axis=1))

        if as_df:
            predictions = pd.DataFrame({'ID_Customer': id_customer, 'PA_Est': np.expm1(predictions)})
            return predictions
        else:
            return np.expm1(predictions)
