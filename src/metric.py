import matplotlib.pyplot as plt
import numpy as np
import os
from stats_util import Type, get_serie

path = os.getcwd()
path
dataset = np.loadtxt(path + "/../data/canary.csv", delimiter=",")
dataset = np.delete(dataset, [1,], axis=1)

fn = get_serie(dataset, Type.qps_eff, None, None)
del dataset


plt.hist(fn, bins=50)
# plt.gca().set_xscale("log", nonposx='clip')
# plt.gca().set_yscale("log", nonposy='clip')
plt.title('rsidual distribution')
plt.xlabel('queue size')
plt.ylabel('auctions');
plt.show()


# In[ ]:
