from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from stats_util import get_cloudwatch_times_serie


figure(num=None, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
x = [0,1,2,3,4,5,6,7,8,9,10,11,12]
b16 = [2892,4658,4986,4119,4357,4267,3767,3523,3186,3142,3538,3696,3818]
b21 = [2679,4588,5040,5013,4894,4822,4686,3992,3900,4114,4265,4253,4560]
b23 = [3092,4326,3744,3991,3685,3381,3121,2776,2866,3270,747,4334,4192]
plt.plot(x,b16, label="b16")
plt.plot(x,b21, label="b21")
plt.plot(x,b23, label="b23")

plt.title('GDNN vs DNN loss through generations')
plt.xlabel('epochs (600 epochs is a new generation for GDNN)')
plt.ylabel('loss');
plt.legend()
plt.show()


time, bids16 = get_cloudwatch_times_serie(datetime(2019, 1, 16,00),datetime(2019, 1, 16,14),'us-east-2','bids')
time, bids21 = get_cloudwatch_times_serie(datetime(2019, 1, 21,00),datetime(2019, 1, 21,14),'us-east-2','bids')
time, bids23 = get_cloudwatch_times_serie(datetime(2019, 1, 23,00),datetime(2019, 1, 23,14),'us-east-2','bids')

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


