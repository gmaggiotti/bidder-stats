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


names = ['predictor_2019-01-18-16:30', 'predictor_2019-01-22-16:30',
         'predictor_2019-01-18-17:30']
predictors = []
for name in names:
    with open(name, 'rb') as f:
        predictors.append(pickle.load(f))

feature_set = set(predictors[0][1]).union(predictors[1][1]).union(predictors[2][1])
preds = [dict(zip(predictors[i][1], predictors[i][2])) for i in range(0, 3)]
as_vectors = {0: [], 1: [], 2: []}

for feature in feature_set:
    [as_vectors[i].append(preds[i].get(feature, 0)) for i in range(0, 3)]

L2 = np.sum(np.subtract(as_vectors[0], as_vectors[1]) ** 2)
print("L2 distance 18 vs 22 {}".format(L2))

L2 = np.sum((np.array(as_vectors[0]) - np.array(as_vectors[2])) ** 2)
print("L2 distance 18 vs 18 {}".format(L2))

diff = np.abs(np.subtract(as_vectors[0], as_vectors[1]))
max_args = diff.argsort()[::-1]

feature_set = np.asarray(feature_set)
print feature_set[max_args]
