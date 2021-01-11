# -*- coding: utf-8 -*-
"""Total population"""
import numpy as np
import csv
import pandas as pd

from helpers import*

class Totalpop:
    
    # Constructor
    def __init__(self, btype, DATA_PATH=None, OUTPUT_PATH=None, location='Switzerland', ti=1950, tf=2020, t0=1950, poptot=None):
        
        # Parameters
        self.t0 = t0
        
        if (btype == 'UN'):
            birth_spline = self.init_UN(DATA_PATH, OUTPUT_PATH, location, ti, tf)
            self.fct = birth_spline
        elif (btype == 'manual'):
            fn = self.init_rect(poptot)
            self.fct = fn
        else:
            print("Error, please enter a type for the birth flux : UN or manual.")
        
     
    
    def init_rect(self, poptot):
        # 
        fn = lambda x: poptot
        return fn
        
    
    def init_UN(self, DATA_PATH, OUTPUT_PATH, location, ti, tf):
        
        # Clean UN data and create the files containing input data for the simulation
        data = load_input(DATA_PATH)
        data = data[['Variant', 'Location', 'Time', 'PopTotal']]
        data[['Time','PopTotal']] = data[['Time','PopTotal']].apply(pd.to_numeric)

        data_loc = data.loc[data['Location'] == location]
        data_loc = data_loc.loc[data_loc['Variant'] == 'Medium']
        data_loc = data_loc.loc[data_loc['Time'] >= ti]
        data_loc = data_loc.loc[data_loc['Time'] <= tf]
    
        dates = np.asarray(data_loc['Time'].drop_duplicates())
        y = np.asarray(data_loc['PopTotal'])
    
        data_file = pd.DataFrame()
        data_file['Time'] = dates
        data_file['PopTotal'] = y
    
        data_file.to_csv(OUTPUT_PATH, index=False) # create input file
        
        poptotal_spline = interpolation1D(OUTPUT_PATH) # creation of the interpolation function
        
        return poptotal_spline
    
        
    # Function that evaluates the interpolation function    
    def evaluate(self, t):
        ret = self.fct(self.t0 + t)
        return ret
        
    # Function that plots the interpolation function at a certain time step 'ind'
    def plot(ind, T, N):
        t = np.linspace(0,T,N+1)
        fig = plt.figure()
        plt.plot(t, self.evaluate(t))
        plt.xlabel('Time [yr]')
        plt.ylabel('Total population [10³ indiv.]')
        
        