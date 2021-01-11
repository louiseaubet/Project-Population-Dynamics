# -*- coding: utf-8 -*-
"""some helper functions"""
import numpy as np
import csv
import pandas as pd
import scipy

from scipy.interpolate import RectBivariateSpline
from scipy.interpolate import interp1d
from sklearn import datasets

# Load the files containing input data as a dataframe
def load_input(DATA_PATH):
    file = pd.read_csv(DATA_PATH)
    df = pd.DataFrame(file)
    return df


# 2D interpolation of the data (for births and deaths)    
def interpolation2D(DATA_PATH, order_x=1, order_y=1):
    data = load_input(DATA_PATH)
    
    y = list(data)
    y = np.asarray(y[1:], dtype=int)
    x = np.asarray(data['Age'])
    z = data.to_numpy()
    z = z[:,1:]

    interp_funct = RectBivariateSpline(x, y, z, kx=order_x, ky=order_y)
    
    return interp_funct


# 1D interpolation of the data (for population)
def interpolation1D(DATA_PATH):
    data = load_input(DATA_PATH)
    
    x = np.asarray(data['Time'])
    y = np.asarray(data.iloc[:,1])
    
    interp_funct = interp1d(x, y, kind='linear')
    
    return interp_funct









    