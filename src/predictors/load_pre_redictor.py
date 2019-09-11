import pickle
import timeit
from functools import reduce

import numpy as np

# Formato predictor:
# Tupla
#   predictor[0]: nombre variables.
#      Ej: ('pais', 'dia')
#   predictor[1]: features como (nombre variables, valor variables)
#      Ej: ((('pais',), ('argentina',)), (('pais', 'dia'), ('usa', 'martes')))
#   predictor[2]: coeficientes features (son floats, comparten el indice con 1
#   predictor[3]: 1

path = '/tmp/macross/prd/'
pre_predictor = path + 'pre_predictor'
predictor = []

with open(pre_predictor, 'rb') as f:
    predictor.append(pickle.load(f))

feature_set = set(predictor[0][1])
preds = dict(zip(predictor[0][1], predictor[0][2]))

as_vectors = [preds.get(feature,0) for feature in feature_set]

L2 = np.sum(np.subtract(as_vectors[0], as_vectors[1]) ** 2)
print("L2 distance 18 vs 22 {}".format(L2))

L2 = np.sum((np.array(as_vectors[0]) - np.array(as_vectors[2])) ** 2)
print("L2 distance 18 vs 18 {}".format(L2))

diff = np.abs(np.subtract(as_vectors[0], as_vectors[1]))
max_args = diff.argsort()[::-1]

feature_set = np.asarray(feature_set)
print feature_set[max_args]
