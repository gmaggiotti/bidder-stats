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
         'predictor_2019-01-18-17:30']
predictors = []
for name in names:
    with open(name, 'rb') as f:
        predictors.append(pickle.load(f))

as_dicts = [{} for _ in predictors]
for d, predictor in zip(as_dicts, predictors):
    for feature, coef in zip(predictor[1], predictor[2]):
        d[feature] = coef

all_features = sorted(
    reduce(lambda s1, s2: s1.union(s2), [set(d) for d in as_dicts], set()))

as_vectors = [np.zeros(len(all_features)) for _ in as_dicts]
for vector, d in zip(as_vectors, as_dicts):
    for i, feature in enumerate(all_features):
        vector[i] = d.get(feature, 0)

L2_fri_tue = np.sum((as_vectors[0] - as_vectors[1])**2)
print("L2 Fri vs Tue: {}".format(L2_fri_tue))

L2_fri_fri = np.sum((as_vectors[1] - as_vectors[2])**2)
print("L2 Fri vs Fri: {}".format(L2_fri_fri))

diff = np.abs(as_vectors[0] - as_vectors[1])
max_args = diff.argsort()[::-1]
all_features = np.asarray(all_features)
print(all_features[max_args[:20]])


import matplotlib.pyplot as plt

s = sorted(diff)
plt.plot(s, label="b23")

plt.title('GDNN vs DNN loss through generations')
plt.xlabel('epochs (600 epochs is a new generation for GDNN)')
plt.ylabel('loss');
plt.legend()
plt.show()