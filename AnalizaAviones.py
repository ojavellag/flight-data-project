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
import numpy as np
import ast

#main function to read and parse kml files
def readPlaneData(DataFileName):
    ff=os.getcwd()+ '/'
    print("the source folder is "+ff)
    dataF = DataFileName    
    existFile=os.path.isfile(dataF)
    if existFile == True:
        print("The file "+DataFileName+" was found!")
    else:
        print("the file doesn't exist!")
    
    tree=et.parse(dataF)
    
    r1 = tree.xpath('.//kml:Placemark/kml:description/text()', namespaces={"kml":"http://www.opengis.net/kml/2.2"})
    r2 = tree.xpath(".//gx:Track/gx:coord/text()",namespaces={"gx":"http://www.google.com/kml/ext/2.2"})
    return r2

#converting data to numeric values
def createMatrix(stringList):
    b=list()
    for i in range(0,len(stringList)):
        c=[float(x) for x in stringList[i].split(' ')]
        b.append(c)
    d=np.array(b)
    return d

def plotTrajectory(coordVect):
    x, y,z = zip(*coordVect)
    plt.scatter(x,y)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x,y,z)
    
    
def preProcessFlight(file_name=""):
    ## apply the function to a file and read the data
    a=readPlaneData(file_name)
    ## Convert data in strings to array of numbers
    b=createMatrix(a)
    # split data into column vectors and plot resutls
    plotTrajectory(b)
    
if __name__ == '__preProcessFlight__':
    preProcessFlight(file_name="")


preProcessFlight(flight.kml)
