from universityhack2018.config import *
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

class FeatureEngineering:
    clients_ = None

    def __init__(self, clients):
        if not isinstance(clients, pd.DataFrame) and not isinstance(clients, pd.Series):
            raise ValueError("The client object must be a pandas DataFrame or Series.")

        self.clients_ = pd.DataFrame({key: pd.Series(clients[key], dtype=value) for (key, value) in DATA_TYPES.items()})


    def polynomial_features(self):
        poly = PolynomialFeatures(2, include_bias=False)
        polynomial_array = poly.fit_transform(self.clients_[TOP_CORRS])
        polynomial_array_cols = poly.get_feature_names(self.clients_[TOP_CORRS].columns)
        polynomial_df = pd.DataFrame(polynomial_array, columns=polynomial_array_cols)

        self.clients_ = self.clients_.drop(TOP_CORRS, axis=1)
        self.clients_ = pd.concat([self.clients_, polynomial_df], axis=1)

        for col in TOP_CORRS:
            self.clients_[col + '^3'] = self.clients_[col] ** 3
            self.clients_['sqrt_' + col] = np.sqrt(self.clients_[col])

        return self.clients_


    def low_skewness(self):
        self.clients_[SKEWED_FEATURES] = np.log1p(self.clients_[SKEWED_FEATURES])

        return self.clients_


    def get_dummies(self):
        cat_feats = self.clients_.select_dtypes(include=[object])
        cat_feats = cat_feats.drop(['ID_Customer', 'Socio_Demo_01'], axis=1)

        cat_feats = pd.DataFrame({key: cat_feats[key].astype('category', categories=value) for (key, value) in CATEGORICAL.items()})

        dummies = pd.get_dummies(cat_feats, drop_first=False)
        dummies = dummies[DUMMIES]
        self.clients_ = self.clients_.drop(cat_feats.columns, axis=1)
        self.clients_ = pd.concat([dummies, self.clients_], axis=1)

        return self.clients_


    def agg_num_feats(self):
        imp_cons = self.clients_.filter(regex='^Imp_Cons_[0-9]+$', axis=1)
        total_imp_cons = imp_cons.apply(lambda x: x.sum(), axis=1)
        mean_imp_cons = imp_cons.apply(lambda x: x.mean(), axis=1)

        imp_sal = self.clients_.filter(regex='^Imp_Sal_[0-9]+$', axis=1)
        total_imp_sal = imp_sal.apply(lambda x: x.sum(), axis=1)
        mean_imp_sal = imp_sal.apply(lambda x: x.mean(), axis=1)

        num_oper = self.clients_.filter(regex='^Num_Oper_[0-9]+$', axis=1)
        total_num_oper = num_oper.apply(lambda x: x.sum(), axis=1)
        mean_num_oper = num_oper.apply(lambda x: x.mean(), axis=1)

        self.clients_ = pd.concat(
            [self.clients_, total_imp_cons, mean_imp_cons, total_imp_sal, mean_imp_sal, total_num_oper, mean_num_oper],
            axis=1)
        names = self.clients_.columns[:-6].tolist()
        names.extend(
            ['Total_Imp_Cons', 'Mean_Imp_Cons', 'Total_Imp_Sal', 'Mean_Imp_Sal', 'Total_Num_Oper', 'Mean_Num_Oper'])
        self.clients_.columns = names

        return self.clients_

    def fill_na(self):
        self.clients_.replace([np.inf, -np.inf], np.nan)
        self.clients_ = self.clients_.fillna(value=FILL_VALUES)

        return self.clients_


    def scale(self):
        for col in self.clients_.isnull().sum()[self.clients_.isnull().sum() > 0].index:
            if self.clients_[col].dtypes != object:
                self.clients_[col] = self.clients_[col].fillna(self.clients_[col].median())

        clients_num = self.clients_.loc[:, NUM_FEATS]
        clients_scaled = self.clients_.drop(NUM_FEATS, axis=1)
        cat_columns = clients_scaled.columns.tolist()
        scaler = STANDARD_SCALER
        clients_num_scaled = scaler.transform(clients_num)
        clients_scaled = np.concatenate((clients_scaled.values, clients_num_scaled), axis=1)
        self.clients_ = pd.DataFrame(clients_scaled, columns=cat_columns+NUM_FEATS)

        return self.clients_
