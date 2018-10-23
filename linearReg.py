# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 18:45:02 2018

@author: broch
"""

import matplotlib.pyplot as plt

pts = [(308, 154), (307, 166), (311, 185), (314, 192), (317, 199), (324, 218), 
          (327, 246), (329, 261), (329, 269), (333, 277), (333, 285), ]#(326, 294), 
         # (343, 304), (339, 315)]
sqrs_x = []
sqrs_y = []
ms_xy = []
x_values = [] 
y_values = []
y_out = []
y_outs = []
for x,y in pts:
    sqr_x = x**2
    sqr_y = y**2
    m_xy = x*y
    
    x_values.append(x)
    y_values.append(y)
    
    ms_xy.append(m_xy)
    sqrs_x.append(sqr_x)
    sqrs_y.append(sqr_y)
    
    sum_x_values = sum(x_values)
    sum_y_values = sum(y_values)
    sum_ms_xy = sum(ms_xy)
    sum_sqrs_x = sum(sqrs_x)
    sum_sqrs_y = sum(sqrs_y)
    
    ave_x = sum_x_values/len(pts)
    ave_y = sum_y_values/len(pts)
    
# y = a + bx    
b = (sum_ms_xy - (len(pts)*ave_x*ave_y) )/(sum_sqrs_x - (len(pts)*(ave_x**2)))
a = ave_y - b*ave_x

for i in range(len(x_values)):
    y = a + b*x_values[i]
    y_out.append(y)
    print(y)

#plt.plot((x_values[0], y_out[0]), ((x_values[13], y_out[13])), 'ro-')
#plt.plot((x_values[0], y_out[0]), (x_values[13], y_out[13]), 'ro-')
plt.scatter(x_values, y_values)
plt.scatter(x_values, y_values)
plt.plot(x_values, y_out)
plt.xlabel('x_values')
plt.ylabel('y_values')
plt.show()
  

###### LIXOOO ########################  
print(x_values[0], y_out[0]) 
print(x_values[10], y_out[10]) 
print('-----')

print(x_values[0], y_values[0]) 
print(x_values[10], y_values[10])   
#print(x)
print('-----')

final_y = a + b*x_values[0]
initial_y = a + b*x_values[10]


initial_pt = (x_values[0], y_out[0])
final_pt = (x_values[10], y_out[10])

print(initial_pt,final_pt)
print((x_values[0], final_y), (x_values[10], initial_y) )

def linearRegression(pts):
    sqrs_x = []
    sqrs_y = []
    ms_xy = []
    x_values = [] 
    y_values = []
    for x,y in pts:
        sqr_x = x**2
        sqr_y = y**2
        m_xy = x*y
        
        x_values.append(x)
        y_values.append(y)
        
        ms_xy.append(m_xy)
        sqrs_x.append(sqr_x)
        sqrs_y.append(sqr_y)
        
        sum_x_values = sum(x_values)
        sum_y_values = sum(y_values)
        sum_ms_xy = sum(ms_xy)
        sum_sqrs_x = sum(sqrs_x)
#        sum_sqrs_y = sum(sqrs_y)
        
        ave_x = sum_x_values/len(pts)
        ave_y = sum_y_values/len(pts)
    
    b = (sum_ms_xy - (len(pts)*ave_x*ave_y) )/(sum_sqrs_x - (len(pts)*(ave_x**2)))
    a = ave_y - b*ave_x
    
    predicted_final_y = a + b*x_values[0]
    predicted_initial_y = a + b*x_values[10]
    
    final_pt = (x_values[0], predicted_final_y)
    initial_pt = (x_values[10], predicted_initial_y)

    return initial_pt, final_pt 
  
inicial, final = linearRegression(pts)  

print(final, inicial)      
        