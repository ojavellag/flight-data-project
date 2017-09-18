#/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 20:50:25 2017

@author: challenger1
"""


import cleanXMLaviones
import numpy as np
import math 
import matplotlib.pyplot as plt
from sklearn import linear_model


fig1=plt.figure()

def dst2line(t,x,px):
    x_t_magn=np.sqrt(x*x+t*t)
    px_t_magn=np.sqrt(px*px+t*t)
    inner_prod=x*px+t*t
    cos_theta = inner_prod/(x_t_magn*px_t_magn)
    sin_theta = np.array([math.sin(math.acos(cos))\
                          for cos in cos_theta]).reshape(-1,1)    
    dst=x*sin_theta
    return dst

#def find_t_ofMin(t,x,px):
#    idx=np.where(x == x.min())
#    a=0
#    t0 = t[idx]
#    for in range(0,len(t)):
#        a+=
#        
#    
#    return t0

#Read the datasets and extract time-series for each coordinate
num_files=13
fg=plt.figure()
for file_idx in range(11,num_files):
    if file_idx==112:
        continue
    st="t%d,x%d,y%d,z%d = cleanXMLaviones.RunPreprocessing(\"flight%d.kml\")"\
    % (file_idx,file_idx,file_idx,file_idx,file_idx)
    exec(st)
    ##fit straigth lines for each spatial component and focus on those for longitude
    st = "pX%d,pY%d,pZ%d = cleanXMLaviones.fitLinearModels(t%d,x%d,y%d,z%d)"\
    % (file_idx,file_idx,file_idx,file_idx,file_idx,file_idx,file_idx)
    exec(st)
    st = "plt.scatter(t%d,x%d,marker=\".\")"% (file_idx,file_idx)
    exec(st)
    st = "plt.plot(t%d,pX%d)"%(file_idx,file_idx)
    exec(st)

fg.set_size_inches(15, fg.get_figheight(), forward=True)
plt.ylabel('long. (deg)')
plt.xlabel('time (s)')   
fg.show()
fg.savefig('flightLong.jpg')    
