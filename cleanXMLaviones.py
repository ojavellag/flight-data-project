#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 18:28:46 2017

@author: Oscar Javier Avella
"""
from __future__ import print_function
import os.path
from lxml import etree as et
import matplotlib.pyplot as plt
from matplotlib.dates import date2num as d2n
from mpl_toolkits.mplot3d import Axes3D
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
import numpy as np
import datetime

#main function to read and parse kml files
def readPlaneData(DataFileName):
    ff=os.getcwd()+ '/'
    #print("the source folder is "+ff)
    dataF = "../DataSets/"+DataFileName    
    existFile=os.path.isfile(dataF)
    if existFile == True:
        print("The file "+DataFileName+" was found!")
    else:
        print("the file doesn't exist!")    
    tree=et.parse(dataF)
    
    #r0 = tree.xpath('.//kml:Placemark/kml:description/text()', namespaces={"kml":"http://www.opengis.net/kml/2.2"})
    r1 = tree.xpath(".//gx:Track/gx:coord/text()",namespaces={"gx":"http://www.google.com/kml/ext/2.2"})
    timeV = tree.xpath('.//kml:when/text()', namespaces={"kml":"http://www.opengis.net/kml/2.2"})
    return r1, timeV

#converting data to numeric values
def createCoordMatrix(stringList):
    b=list()
    for i in range(0,len(stringList)):
        c=[float(x) for x in stringList[i].split(' ')]
        b.append(c)
    d=np.array(b)
    return d

def readTime(timeList):
    timeV=list()
    for i in range(len(timeList)):
        timeV.append(datetime.datetime.strptime(timeList[i], "%Y-%m-%dT%H:%M:%SZ").timestamp())
    timeV = [t - timeV[0] for t in timeV]                
    return timeV

def ExtractXYZ(coordVect):
    x, y,z = zip(*coordVect)    
    return x,y,z

def plotTrajectory(x,y,z,T):
    fig=plt.figure()
    ax1 = fig.add_subplot(311)    
    plt.scatter(T,z)
    ax1.xaxis.set_visible(False)
    ax1.set_ylabel('alt. (m)')
    
    ax2 = fig.add_subplot(312)
    ax2.set_ylabel('latt. (deg)')
    ax2.xaxis.set_visible(False)
    plt.scatter(T,y)
    plotTrajectory
    ax3 = fig.add_subplot(313)
    ax3.set_ylabel('long. (deg)')
    ax3.set_xlabel('time (s)')
    plt.scatter(T,x)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x,y,z)

def RunPreprocessing(dataset=""):
    ## apply the function to a file and read the data
    a1,a2=readPlaneData(dataset)
    ## Convert data in strings to array of numbers
    b=createCoordMatrix(a1)
    ## extract the time component
    time_=readTime(a2)
    # split data into column vectors and plot resutls
    x,y,z = ExtractXYZ(b)
    # check the plane's trajectory in each 3D direction    
    #plotTrajectory(x,y,z,time_)#UNCOMMENT THIS LINE TO SEE PLOTS!!
    # store data into arrays for processing
    time_ = np.array(time_).reshape(-1,1)
    x = np.array(x).reshape(-1,1)   
    y = np.array(y).reshape(-1,1)    
    z = np.array(z).reshape(-1,1)
    return time_,x,y,z
    
def fitLinearModels(t,x,y,z):
    cX=np.column_stack((t,t*t,t*t*t,t*t*t*t))
    cZ=np.column_stack((t,t*t))
    model = LinearRegression()
    model.fit(cX,x)
    predX = model.predict(cX)
    model.fit(t,y)
    predY = model.predict(t)
    model.fit(cZ,z)
    predZ = model.predict(cZ)
    return predX,predY,predZ

    