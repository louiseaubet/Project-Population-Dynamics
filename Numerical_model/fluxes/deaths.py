# -*- coding: utf-8 -*-
"""definitions of the death flux"""
import numpy as np
import csv
import pandas as pd

from helpers import*


class Deaths:
    
    # Constructor
    def __init__(self, btype, DATA_PATH=None, OUTPUT_PATH=None, location='Switzerland', ti=1950, tf=2020, t0=1950, mu=0.01):
        
        # Parameters
        self.t0 = t0
        
        if (btype == 'UN'):
            birth_spline = self.init_UN(DATA_PATH, OUTPUT_PATH, location, ti, tf)
            self.fct = birth_spline
        elif (btype == 'manual'):
            fn = self.init_rect(mu)
            self.mu = mu
            self.fct = fn
        else:
            print("Error, please enter a type for the birth flux : UN or manual.")
   

    def init_rect(self, mu):
        fn = lambda x: np.exp(0.07*(x-20))*0.001 + 0.03*np.exp(-x**2/10)
        return fn
        
        
    
    def init_UN(self, DATA_PATH, OUTPUT_PATH, location, ti, tf):
        
        # Clean UN data and create the files containing input data for the simulation
        data = load_input(DATA_PATH)
        data = data[['Location', 'MidPeriod', 'Sex', 'AgeGrpStart', 'mx']]
        data[['MidPeriod', 'AgeGrpStart', 'mx']] = data[['MidPeriod', 'AgeGrpStart', 'mx']].apply(pd.to_numeric)
        data = data.loc[data['Sex'] == 'Total']
        data[['MidPeriod']] = data[['MidPeriod']].subtract(3) #MidPeriod -> Start of the period
        data.columns = ['Location', 'Time', 'Sex', 'AgeGrpStart', 'mx'] #rename column 'MidPeriod' -> 'Time'
        data = data.replace(np.nan,1)
    
        data_loc = data.loc[data['Location'] == location]
        data_loc = data_loc.loc[data_loc['Time'] >= ti]
        data_loc = data_loc.loc[data_loc['Time'] <= tf]

        dates = np.asarray(data_loc['Time'].drop_duplicates())
        ages = np.asarray(data_loc['AgeGrpStart'].drop_duplicates())
    
        data_file = pd.DataFrame()
        data_file['Age'] = ages
    
        for i in range (0,len(dates)):
            samples = data_loc.loc[data_loc['Time'] == dates[i]]
            y = np.asarray(samples['mx'])
            data_file[str(dates[i])] = y
        
        data_file.to_csv(OUTPUT_PATH, index=False) # create input file
        
        death_spline = interpolation2D(OUTPUT_PATH, 1, 1) # creation of the interpolation function
        
        return death_spline
        
        
    # Function that evaluates the interpolation function     
    def evaluate(self, x, t):
        ret = self.fct(x, self.t0 + t)
        return ret 
    
    # Function that plots the interpolation function at a certain time step 'ind'
    def plot(self, ind, A, M):
        a = np.linspace(0,A,M+1)
        fig = plt.figure()
        plt.plot(a, self.evaluate(a, ind))
        plt.xlabel('Age [yr]')
        plt.ylabel('Death rate [ ]')
    
    # Function that defines the survival probability
    def pi(self, x, t, M):
        Isum = 0
        N = 50
        d = x/(M-1)
        for i in range(0,M):
            Isum += (self.evaluate(i*d, t) + self.evaluate((i+1)*d, t))/2
        ret = np.exp(- d*Isum)
        return ret
        
        
        
        
        