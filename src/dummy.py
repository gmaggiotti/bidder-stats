from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from stats_util import get_cloudwatch_times_serie

stats = 'Average'

time, cap = get_cloudwatch_times_serie(datetime(2019, 1, 26, 00), datetime(2019, 1, 26, 22), 'us-east-2', 'cap',stats)
time, eff = get_cloudwatch_times_serie(datetime(2019, 1, 26, 00), datetime(2019, 1, 26, 22), 'us-east-2', 'eff',stats)


plt.plot(time, cap, label="cap")
plt.plot(time, eff, label="eff")

plt.title('qps')
plt.xlabel('cap and eff serie')
plt.ylabel('freq');
plt.legend()
plt.show()

time, bids = get_cloudwatch_times_serie(datetime(2019, 1, 26, 00), datetime(2019, 1, 26, 22), 'us-east-2', 'bids',stats)


plt.plot(time, bids, label="bids")

plt.title('bids')
plt.xlabel('bids serie')
plt.ylabel('loss');
plt.legend()
plt.show()


# print np.sum(b16)
# print np.sum(b21)
# print np.sum(b23)
# print 1- np.sum(b23)/ float(np.sum(b16))
# print 1- np.sum(b23)/ float(np.sum(b21))
#
# a = np.arange(16).reshape(4,4)
# b = np.arange(4)
# c = np.arange(6).reshape(2,3)
#
# r1 = np.einsum('ij,j', a, b)
#
# x1 = np.inner(a,a)
# x2 = np.dot(a,a)


