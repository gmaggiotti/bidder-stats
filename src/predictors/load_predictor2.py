import pickle

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
         'predictor_2019-01-22-17:30']
predictors = []
for name in names:
    with open(name, 'rb') as f:
        predictors.append(pickle.load(f))

feature_set = set()
for predictor in predictors:
    for feature in predictor[1]:
        feature_set.add(feature)

pred1 = []
for feature in feature_set:
    try:
        idx = predictors[0][1].index(feature)
        pred1.append(predictors[0][2][idx])
    except ValueError as v:
        pred1.append(0)

as_dicts = [{} for _ in predictors]
for d, predictor in zip(as_dicts, predictors):
    for feature, coef in zip(predictor[1], predictor[2]):
        d[feature] = coef
