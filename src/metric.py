#!/usr/bin/env python
# coding: utf-8

# # Residual Histogram
# ## Creating an histogram from residual to see queue legnth distribution

# run html

# In[19]:

import matplotlib.pyplot as plt
import numpy as np
import os

path = os.getcwd()
path 
dataset = np.loadtxt(path + "/../data/metric.csv", delimiter=",")
fn = dataset[:,3]


#plt.plot(dataset[1])
plt.hist(fn,bins=50)
# plt.gca().set_xscale("log", nonposx='clip')
# plt.gca().set_yscale("log", nonposy='clip')
plt.title('rsidual distribution')
plt.xlabel('queue size')
plt.ylabel('auctions');
plt.show()


# In[ ]:




