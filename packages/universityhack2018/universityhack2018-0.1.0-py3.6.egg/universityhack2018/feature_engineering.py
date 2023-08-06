import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures

class FeatureEngineering:
    # @var pd.DataFrame
    client_ = None
    # @var dict
    data_types_ = {'ID_Customer': 'object', 'Imp_Cons_01': 'float64', 'Imp_Cons_02': 'float64',
                   'Imp_Cons_03': 'float64', 'Imp_Cons_04': 'float64', 'Imp_Cons_05': 'float64',
                   'Imp_Cons_06': 'float64', 'Imp_Cons_07': 'float64', 'Imp_Cons_08': 'float64',
                   'Imp_Cons_09': 'float64', 'Imp_Cons_10': 'float64', 'Imp_Cons_11': 'float64',
                   'Imp_Cons_12': 'float64', 'Imp_Cons_13': 'float64', 'Imp_Cons_14': 'float64',
                   'Imp_Cons_15': 'float64', 'Imp_Cons_16': 'float64', 'Imp_Cons_17': 'float64',
                   'Imp_Sal_01': 'float64', 'Imp_Sal_02': 'float64', 'Imp_Sal_03': 'float64',
                   'Imp_Sal_04': 'float64', 'Imp_Sal_05': 'float64', 'Imp_Sal_06': 'float64',
                   'Imp_Sal_07': 'float64', 'Imp_Sal_08': 'float64', 'Imp_Sal_09': 'float64',
                   'Imp_Sal_10': 'float64', 'Imp_Sal_11': 'float64', 'Imp_Sal_12': 'float64',
                   'Imp_Sal_13': 'float64', 'Imp_Sal_14': 'float64', 'Imp_Sal_15': 'float64',
                   'Imp_Sal_16': 'float64', 'Imp_Sal_17': 'float64', 'Imp_Sal_18': 'float64',
                   'Imp_Sal_19': 'float64', 'Imp_Sal_20': 'float64', 'Imp_Sal_21': 'float64',
                   'Ind_Prod_01': 'object', 'Ind_Prod_02': 'object', 'Ind_Prod_03': 'object',
                   'Ind_Prod_04': 'object', 'Ind_Prod_05': 'object', 'Ind_Prod_06': 'object',
                   'Ind_Prod_07': 'object', 'Ind_Prod_08': 'object', 'Ind_Prod_09': 'object',
                   'Ind_Prod_10': 'object', 'Ind_Prod_11': 'object', 'Ind_Prod_12': 'object',
                   'Ind_Prod_13': 'object', 'Ind_Prod_14': 'object', 'Ind_Prod_15': 'object',
                   'Ind_Prod_16': 'object', 'Ind_Prod_17': 'object', 'Ind_Prod_18': 'object',
                   'Ind_Prod_19': 'object', 'Ind_Prod_20': 'object', 'Ind_Prod_21': 'object',
                   'Ind_Prod_22': 'object', 'Ind_Prod_23': 'object', 'Ind_Prod_24': 'object',
                   'Num_Oper_01': 'int64', 'Num_Oper_02': 'int64', 'Num_Oper_03': 'int64',
                   'Num_Oper_04': 'int64', 'Num_Oper_05': 'int64', 'Num_Oper_06': 'int64',
                   'Num_Oper_07': 'int64', 'Num_Oper_08': 'int64', 'Num_Oper_09': 'int64',
                   'Num_Oper_10': 'int64', 'Num_Oper_11': 'int64', 'Num_Oper_12': 'int64',
                   'Num_Oper_13': 'int64', 'Num_Oper_14': 'int64', 'Num_Oper_15': 'int64',
                   'Num_Oper_16': 'int64', 'Num_Oper_17': 'int64', 'Num_Oper_18': 'int64',
                   'Num_Oper_19': 'int64', 'Num_Oper_20': 'int64', 'Socio_Demo_01': 'object',
                   'Socio_Demo_02': 'object', 'Socio_Demo_03': 'float64', 'Socio_Demo_04': 'int64',
                   'Socio_Demo_05': 'int64'}
    # @var list
    top_corrs_ = ['Imp_Sal_08', 'Imp_Sal_21', 'Imp_Sal_09', 'Imp_Sal_19', 'Num_Oper_06', 'Num_Oper_05',
                  'Imp_Sal_12', 'Imp_Cons_06', 'Imp_Cons_12', 'Num_Oper_18']

    def __init__(self, client):
        if not client:
            raise ValueError("A client array must be specified.")
        if not isinstance(client, pd.DataFrame) or not isinstance(client, np.ndarray):
            raise ValueError("The client object must be a pandas DataFrame or numpy ndarray.")

        self.client_ = client

        if isinstance(client, np.ndarray):
            self.client_ = pd.DataFrame(self.client_, names=list(self.data_types_.keys()),
                                        dtype=self.data_types_)

    def polynomial_features(self):
        poly = PolynomialFeatures(2, include_bias=False)
        polynomial_array = poly.fit_transform(self.client_[self.top_corrs_])
        polynomial_array_cols = poly.get_feature_names(self.client_[self.top_corrs_].columns)
        polynomial_df = pd.DataFrame(polynomial_array, columns=polynomial_array_cols)

        self.client_ = self.client_.drop(self.top_corrs_, axis=1)
        self.client_ = pd.concat([self.client_, polynomial_df], axis=1)

        for col in self.top_corrs_:
            self.client_[col + '^3'] = self.client_[col] ** 3
            self.client_['sqrt_' + col] = np.sqrt(self.client_[col])


