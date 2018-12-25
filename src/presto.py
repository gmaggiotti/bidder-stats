from stats_util import get_presto_bidrate_histogram
import numpy as np
from scipy import stats
#hist = get_presto_bidrate_histogram(24,"20181210","20181210")
hist = None
x= [1,2.4,3]
y= [10,30,10]

x=[23,24,25,26,27,28,29,30,31]
y=[3,7,13,18,23,17,8,6,5]
y1=[3,7,13,19,23,17,8,6,5]

n = np.sum(y)
mean = np.dot(x,y)/float(n)
standar_dsviation = np.sqrt(np.sum( (x - mean)**2 * np.array(y)) / float(n))

# rejection region
alfa = 0.01

dice = np.array([y,y1])
stats.chi2_contingency(dice)
chi2_stat, p_val, dof, ex = stats.chi2_contingency(dice)
print(mean)

