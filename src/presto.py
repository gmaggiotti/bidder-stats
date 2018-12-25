from stats_util import get_presto_bidrate_histogram
import numpy as np
#hist = get_presto_bidrate_histogram(24,"20181210","20181210")
hist = None
x= [1,2.4,3]
y= [10,30,10]

x=[23,24,25,26,27,28,29,30,31]
y=[3,7,13,18,23,17,8,6,5]

n = np.sum(y)
mean = np.dot(x,y)/float(n)
standar_dsviation = np.sqrt(np.sum( (np.array(x) - mean)**2 * np.array(y)) / float(n))


print(mean)

