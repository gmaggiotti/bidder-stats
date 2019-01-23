import pickle

#nota, el que dice 2018-01-22 17:30, en realidad es del 18 de enero

names = ['predictor_2019-01-18-16:30', 'predictor_2019-01-22-16:30',
         'predictor_2019-01-22-17:30']
predictors = []
for name in names:
    with open(name, 'rb') as f:
        predictors.append(pickle.load(f))

predictors
# Formato predictor:
# Tupla
#   predictor[0]: nombre variables.
#      Ej: ('pais', 'dia')
#   predictor[1]: features como (nombre variables, valor variables)
#      Ej: ((('pais',), ('argentina',)), (('pais', 'dia'), ('usa', 'martes')))
#   predictor[2]: coeficientes features (son floats, comparten el indice con 1
#   predictor[3]: 1
