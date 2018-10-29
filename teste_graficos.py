# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 12:52:46 2018

@author: broch
"""

import numpy as np
import matplotlib.pyplot as plt



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


# the histogram of the data
#plt.figure(0)
#plt.plot(abs_error, 'o-')
plt.figure(1)
plt.plot(erro_3km, '.')

a = 'start'
b = 'dw231233'
c = 'edw'
d = 'Hisam of IQ'
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ = ' + f'{a:>15}\n' +
          f'{d:<14} = ' + f'{b:>15}\n' +
          'Histogram of IQdsadasd = ' + f'{c:>15}\n' +
          'kjjhk')
#plt.text(0.05, 10, 'teste')
plt.grid(True)
plt.show()

#plt.figure(5, figsize=[9,6])
#x = [-0.7, 2.53, -0.41, 5.57, -0.43, 0.66, -8.86, -8.28, -11.6, 1.91, -8.69, -4.09, -0.14, 0.74, 3.71, 6.56, 4.14, 0.29, 2.4, 3.73, -6.23, 2.69]
#abs_list = []
#for value in x:
#    abs_list.append(abs(value))
#
#plt.plot([0, len(abs_list) + 3], [0, 0], color='k', linestyle='-', linewidth=1)
#plt.plot([0, len(abs_list) + 3], [3, 3], color='k', linestyle=':', linewidth=1)
#plt.plot([0, len(abs_list) + 3], [5, 5], color='k', linestyle='--', linewidth=1)
#
#plt.plot(sorted(abs_list), 'ro-')
#plt.savefig('results/asd.png')


