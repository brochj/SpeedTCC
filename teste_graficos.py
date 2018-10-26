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
x = [54.76, 52.39, 54.23, 52.86, 51.12, 56.01, 48.89, 49.06, 53.74, 56.65, 0]

# the histogram of the data
plt.plot(x)


plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.grid(True)
plt.show()