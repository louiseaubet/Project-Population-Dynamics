# -*- coding: utf-8 -*-
"""definitions of the population fluxes"""
import numpy as np
import csv
import pandas as pd

from helpers import*


class Births:

    # Constructor
    def __init__(self, btype, DATA_PATH=None, OUTPUT_PATH=None, location='Switzerland', ti=1950, tf=2020, t0=1950, TFR=2.31):
        
        # Parameters
        self.t0 = t0
        
        if (btype == 'UN'):
            birth_spline = self.init_UN(DATA_PATH, OUTPUT_PATH, location, ti, tf)
            self.fct = birth_spline
        elif (btype == 'manual'):
            fn = self.init_rect(TFR)
            self.TFR = TFR
            self.fct = fn
        else:
            print("Error, please enter a type for the birth flux : UN or manual.")
        
     
    
    def init_rect(self, TFR):
        fn = lambda x: TFR*( np.heaviside(x-15,1) - np.heaviside(x-45,1) )/(2*30)
        return fn
        
    
    def init_UN(self, DATA_PATH, OUTPUT_PATH, location, ti, tf):
        # Clean UN data and create the files containing input data for the simulation
        data = load_input(DATA_PATH)
        data = data[['Variant', 'Location', 'MidPeriod', 'AgeGrpStart', 'ASFR']]
        data[['MidPeriod','AgeGrpStart','ASFR']] = data[['MidPeriod','AgeGrpStart','ASFR']].apply(pd.to_numeric)
        data[['MidPeriod']] = data[['MidPeriod']].subtract(3) #MidPeriod -> Start of the period
        data.columns = ['Variant', 'Location', 'Time', 'AgeGrpStart', 'ASFR'] #rename column 'MidPeriod'->'Time'
    
        data_loc = data.loc[data['Location'] == location]
        data_loc = data_loc.loc[data_loc['Variant'] == 'Medium']
        data_loc = data_loc.loc[data_loc['Time'] >= ti]
        data_loc = data_loc.loc[data_loc['Time'] <= tf]
    
        dates = np.asarray(data_loc['Time'].drop_duplicates())
        ages = np.linspace(0,100,21)
    
        data_file = pd.DataFrame()
        data_file['Age'] = ages

        for i in range (0,len(dates)):
            data_loc_i = data_loc.loc[data_loc['Time'] == dates[i]]
            y = np.pad(data_loc_i['ASFR'], (3, 11), 'constant', constant_values=(0, 0))
            y /= 1000
            data_file[str(dates[i])] = y
        
        data_file.to_csv(OUTPUT_PATH, index=False) # create input file
    
        birth_spline = interpolation2D(OUTPUT_PATH, 1, 1) # creation of the interpolation function
        
        return birth_spline
        
        
    # Function that evaluate the interpolation function
    def evaluate(self, x, t):
        ret = 0.5*self.fct(x, self.t0 + t)
        return ret

    # Function that plots the interpolation function at a certain time step 'ind'
    def plot(self, ind, A, M):
        a = np.linspace(0,A,M+1)
        fig = plt.figure()
        plt.plot(a, self.evaluate(a, ind))
        plt.xlabel('Age [yr]')
        plt.ylabel('ASFR [ ]')



