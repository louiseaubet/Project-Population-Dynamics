# -*- coding: utf-8 -*-
"""population"""
import numpy as np
import csv
import pandas as pd

from helpers import*


class Population:
    
    # Constructor
    def __init__(self, btype, DATA_PATH=None, OUTPUT_PATH=None, location='Switzerland', ti=1950, tf=2020, t0=1950, pop=None):
        
        # Parameters
        self.t0 = t0
        
        if (btype == 'UN'):
            birth_spline = self.init_UN(DATA_PATH, OUTPUT_PATH, location, ti, tf)
            self.fct = birth_spline
        elif (btype == 'manual'):
            fn = self.init_rect(pop)
            self.pop = pop
            self.fct = fn
        else:
            print("Error, please enter a type for the birth flux : UN or manual.")
        
     
    
    def init_rect(self, pop):
        fn = lambda x: pop
        return fn
        
    
    def init_UN(self, DATA_PATH, OUTPUT_PATH, location, ti, tf):
        # Clean UN data and create the files containing input data for the simulation
        data = load_input(DATA_PATH)
        data = data[['Location', 'Time', 'AgeGrpStart', 'PopTotal']]
        data[['Time','AgeGrpStart','PopTotal']] = data[['Time','AgeGrpStart','PopTotal']].apply(pd.to_numeric)
    
        data_loc = data.loc[data['Location'] == location]
        data_loc = data_loc.loc[data_loc['Time'] >= ti]
        data_loc = data_loc.loc[data_loc['Time'] <= tf]
    
        dates = np.asarray(data_loc['Time'].drop_duplicates())
        ages = np.asarray(data_loc['AgeGrpStart'].drop_duplicates())
    
        data_file = pd.DataFrame()
        data_file['Age'] = ages

        for i in range (0,len(dates)):
            samples = data_loc.loc[data_loc['Time'] == dates[i]]
            y = np.asarray(samples['PopTotal'])
            y /= 5
            data_file[dates[i]] = y
    
        data_file.to_csv(OUTPUT_PATH, index=False) # create input file
        
        pop_spline = interpolation2D(OUTPUT_PATH, 1, 1) # creation of the interpolation function
        
        return pop_spline
        
        
    # Function that evaluate the interpolation function
    def evaluate(self, x, t):
        ret = self.fct(x, self.t0 + t)
        return ret
        
    # Function that plots the interpolation function at a certain time step 'ind'    
    def plot(self, ind, A, M):
        a = np.linspace(0,A,M+1)
        fig = plt.figure()
        plt.plot(a, self.evaluate(a, ind))
        plt.xlabel('Age [yr]')
        plt.ylabel('True population repartition [10³ indiv.]')
        
        
        