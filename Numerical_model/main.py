# -*- coding: utf-8 -*-
"""Main function"""
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
import scipy

plt.close('all')
from matplotlib import rcParams, cycler

from helpers import *
from scheme import*

###################################

def main(location, ti, tf, t0, h, A):
    
    births, deaths, pop, totalpop = input_flux(location, ti, tf, t0)
    
    scheme = Scheme(t0, tf, h, A, births, deaths, pop, totalpop)
    
    scheme.run()
    fig1 = scheme.plot_P()
    fig2 = scheme.plot_Ptot()
    #scheme.plot_Pw()
    fig3 = scheme.plot_comparison(70)
    
    print("Done")
    
###################################


def main_convergence(location, ti, tf, t0, h, A):
    
    # Function that verify the convergence of the algorithm
    
    births, deaths, pop, totalpop = input_flux(location, ti, tf, t0)
    
    scheme = Scheme(t0, tf, h, A, births, deaths, pop, totalpop)
    
    hv = [1.7/3, 1.2/3, 1.0/3, 0.75/3, 0.5/3, 0.1/3, 0.05/3] # length time interval [years]
    time_step=18
        
    Err = np.zeros((len(hv), 1))
    index = np.zeros((len(hv), 1))
        
    for k in range(0,len(hv)):
        h = hv[k]
        scheme = Scheme(t0, tf, h, A, births, deaths, pop, totalpop)
        scheme.run()
        diff = abs(scheme.P[:,time_step]-scheme.pop.evaluate(scheme.a, time_step)) / abs(scheme.pop.evaluate(scheme.a, time_step))
        Err[k] = np.max(diff)
        index[k] = np.argmax(diff)
    
    fig = plt.figure()
    plt.loglog(hv, Err, label='error')
    plt.loglog(hv, np.power(hv,3), label='h³')
    plt.xlabel('h [yr]')
    plt.ylabel('Error [10³ indiv.]')
    plt.legend(loc ='lower right')

    print("Done")
    

###################################

def input_flux(location, ti, tf, t0):
    
    DATA_BIRTHS_PATH = "data/fertility_indicators.csv"
    INPUT_BIRTHS_PATH = "inputs/ASFR_PH.csv"

    DATA_DEATHS_PATH = "data/life_table.csv"
    INPUT_DEATHS_PATH = "inputs/mx_PH.csv"

    DATA_POP_PATH = "data/population_by_age.csv"
    INPUT_POP_PATH = "inputs/population_PH.csv"

    DATA_POPTOT_PATH = "data/total_population.csv"
    INPUT_POPTOT_PATH = "inputs/totalpop_PH.csv"
    
    births = Births(btype='UN', DATA_PATH=DATA_BIRTHS_PATH, OUTPUT_PATH=INPUT_BIRTHS_PATH, location=location, ti=ti, tf=tf, t0=t0)
    deaths = Deaths(btype='UN', DATA_PATH=DATA_DEATHS_PATH, OUTPUT_PATH=INPUT_DEATHS_PATH, location=location, ti=ti, tf=tf, t0=t0)
    pop = Population(btype='UN', DATA_PATH=DATA_POP_PATH, OUTPUT_PATH=INPUT_POP_PATH, location=location, ti=ti, tf=tf, t0=t0)
    totalpop = Totalpop(btype='UN', DATA_PATH=DATA_POPTOT_PATH, OUTPUT_PATH=INPUT_POPTOT_PATH, location=location, ti=ti, tf=tf, t0=t0)
    
    return births, deaths, pop, totalpop
    

###################################
    
if __name__ == "__main__":
    main()
    
    