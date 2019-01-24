from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from stats_util import get_cloudwatch_times_serie

time, bids16 = get_cloudwatch_times_serie(datetime(2019, 1, 16,00),datetime(2019, 1, 16,21),'us-east-2','bids')
time, bids21 = get_cloudwatch_times_serie(datetime(2019, 1, 21,00),datetime(2019, 1, 21,21),'us-east-2','bids')
time, bids23 = get_cloudwatch_times_serie(datetime(2019, 1, 23,00),datetime(2019, 1, 23,21),'us-east-2','bids')

plt.plot(time,bids16, label="b16")
plt.plot(time,bids21, label="b21")
plt.plot(time,bids23, label="b23")

plt.title('GDNN vs DNN loss through generations')
plt.xlabel('epochs (600 epochs is a new generation for GDNN)')
plt.ylabel('loss');
plt.legend()
plt.show()


print np.sum(b16)
print np.sum(b21)
print np.sum(b23)
print 1- np.sum(b23)/ float(np.sum(b16))
print 1- np.sum(b23)/ float(np.sum(b21))

a = np.arange(16).reshape(4,4)
b = np.arange(4)
c = np.arange(6).reshape(2,3)

r1 = np.einsum('ij,j', a, b)

x1 = np.inner(a,a)
x2 = np.dot(a,a)


