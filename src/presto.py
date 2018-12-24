from stats_util import get_presto_bidrate_histogram
import numpy as np
#hist = get_presto_bidrate_histogram(24,"20181210","20181210")
hist = None
x= [1,2.4,3]
y= [10,30,10]


n = np.sum(y)
mean = np.dot(x,y)/n
standar_dsviation = np.sqrt(np.sum(np.power((np.array(x) - mean), 2) * np.array(y)) / n)

print(mean)

print var
