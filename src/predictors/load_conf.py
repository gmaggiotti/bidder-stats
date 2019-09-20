import pickle



names = ['/home/gabe/Downloads/config','/home/gabe/Downloads/config1','/home/gabe/Downloads/config2']
predictors = []
for name in names:
    with open(name, 'rb') as f:
        predictors.append(pickle.load(f))

print('a')


# pickle.dump(value, file, protocol=2)