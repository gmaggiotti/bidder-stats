from stats_util import get_presto_bidrate_histogram
import numpy as np
from scipy import stats
#hist = get_presto_bidrate_histogram(24,"20181210","20181210")
hist = None
x           =[40, 52, 63, 80, 95, 110, 126, 146, 169, 199, 234, 288]
x_silver    =[36, 48, 61, 80, 92, 104, 116, 130, 144, 161, 184, 212]

y_silver = np.array([19667, 27522, 25093, 15509, 23275, 34854, 35016, 28113, 19415, 14404, 9920, 6375]) / 1000

y        = np.array([39982, 20155, 14826, 17286, 28161, 36395, 34319, 29445, 16653, 11083, 7866, 3016])/ 1000

n = np.sum(y)
mean = np.dot(x, y) / float(n)
standar_dsviation = np.sqrt(np.sum((x - mean) ** 2 * np.array(y)) / float(n))

# rejection region
alfa = 0.01

dice = np.array([y,y_silver])
stats.chi2_contingency(dice)
chi2_stat, p_val, dof, ex = stats.chi2_contingency(dice)
print(p_val)

