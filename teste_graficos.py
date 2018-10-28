# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 12:52:46 2018

@author: broch
"""

import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(19680801)

mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)
x = [54.76, 52.39, 54.23, 52.86, 51.12, 56.01, 48.89, 49.06, 53.74, 56.65]
y = [53.36, 56.19, 53.33, 58.16, 52.62, 50.61, 42.19, 46.86, 54.44, 53.15]
x2 = []
y2 = []
abs_error = []
erro_3km = []

for i in range(len(x)):
    if x[i] > 50 and x[i] < 54:
        x2.append(x[i])
        y2.append(y[i])
        
    abs_error.append(round(x[i]-y[i], 4))
    erro_3km.append((3,-3))

d1 = {}
d1['unique_id'] = dict(speeds=[1323,213,213,213,213], id2=123)   

# the histogram of the data
plt.plot(abs_error)
plt.plot(erro_3km)


plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title(f'Histogram of IQ {round(np.mean(abs_error), 5)}')
plt.text(0.05, 10, 'teste')
plt.grid(True)
plt.show()