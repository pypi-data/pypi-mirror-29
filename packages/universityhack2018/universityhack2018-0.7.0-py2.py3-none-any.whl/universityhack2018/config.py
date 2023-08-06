import pickle
import os

def load_object(filename):
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'objects/' + filename)
    with open(filename, 'rb') as input:
        return pickle.load(input)

DATA_TYPES = load_object('data_types.pkl')

TOP_CORRS = load_object('top_corrs.pkl')

SKEWED_FEATURES = load_object('skewed_features.pkl')

CATEGORICAL = load_object('categorical.pkl')

REMOVE = load_object('remove.pkl')

DUMMIES = load_object('dummies.pkl')

FILL_VALUES = load_object('fill_values.pkl')

NUM_FEATS = load_object('num_feats.pkl')

STANDARD_SCALER = load_object('standard_scaler.pkl')
