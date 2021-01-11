# -*- coding: utf-8 -*-
"""Numerical model"""
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams, cycler

from helpers import *
from fluxes.births import *
from fluxes.deaths import *
from fluxes.population import *
from fluxes.totalpop import *


class Scheme:
    
    def __init__(self, t0, tf, h, A, births, deaths, pop, totalpop):
        self.t0 = t0
        self.tf = tf
        self.h = h
        self.A = A
        self.T = tf-t0
        self.M = int(A/h) # M+1 = number of data points in age 
        self.N = int(self.T/h) # N+1 = number of data points in time
        self.a = np.linspace(0,self.A,self.M+1)
        self.t = np.linspace(0,self.T,self.N+1)
        self.births = births
        self.deaths = deaths
        self.pop = pop
        self.totalpop = totalpop
        self.P = np.zeros((self.M+1,self.N+1)) 
        self.women = np.zeros((self.N+1,1))
        self.Ptot = np.zeros((self.N+1,1))
        
        
    def run(self):
        
        # Initial condition
        p0 = np.asarray(self.pop.evaluate(self.a, 0)).ravel()
        self.P[:,0] = p0 # initial population repartition
        P_zero = np.where((self.a>=15)&(self.a<=45), self.P[:,0], 0) #repartition of women in fertility period
        self.women[0] = np.sum(P_zero)
        self.Ptot[0] = np.sum(self.P[:,0])

        for n in range(0,self.N): # loop on time
            
            for i in range(0,self.M): # loop on age
                Mu = self.deaths.evaluate(self.a[i]+self.h/2, self.t[n]) # evaluation of the death function
                self.P[i+1,n+1] = self.P[i,n]*( (2 - self.h*Mu) / (2 + self.h*Mu) )
        
            # Boundary condition
            sum_init = 0
            for i in range(1,self.M):
                sum_init += self.births.evaluate(self.a[i],self.t[n+1])*self.P[i,n]
                
            self.P[0,n+1] = (2*self.h*sum_init + self.h*self.births.evaluate(self.a[self.M],self.t[n+1])*self.P[self.M,n+1]) / (2 - self.h*self.births.evaluate(self.a[0],self.t[n+1]))
    
            # Fertile women and total population
            P_zero = np.where((self.a>=15)&(self.a<=45), self.P[:,n+1], 0)
            self.women[n+1] = np.sum(P_zero)
            self.Ptot[n+1] = np.sum(self.P[:,n+1])
            
    
    # Function that plots the population repartition every 10 years    
    def convergence(self):
        
        hv = [1.7/3, 1.2/3, 1.0/3, 0.75/3, 0.5/3, 0.1/3, 0.05/3] # length time interval [years]
        Err = np.zeros((len(hv), 1))
        err = np.zeros((len(hv), 1))
        P_norm = np.zeros((len(hv), 1))
        index = np.zeros((len(hv), 1))
        
        for k in range(0,len(hv)):
    
            h = hv[k]

            time_step=18
            diff = abs(P[:,time_step]-P_true[:,time_step])/abs(P_true[:,time_step])
            Err[k] = max(diff)
            index[k] = np.argmax(diff)
        

    # Function that plots the population repartition every 10 years    
    def plot_P(self):
        fig = plt.figure()
        
        # definition of the colours
        cmap = plt.cm.coolwarm
        num_curve = self.N/10 + 1
        rcParams['axes.prop_cycle'] = cycler(color=cmap(np.linspace(0, 1, num_curve)))

        #plt.plot(self.a, self.P[:,0], label=self.t[0])
        for n in range(0,self.N+1): # loop on time
            if(0 == np.mod(n,10)):
                plt.plot(self.a, self.P[:,n], label=self.t[n])

        plt.xlabel('Age [yr]')
        plt.ylabel('Population repartition [10³ indiv.]')
        plt.legend(loc = 'upper right')
        fig.savefig('outputs/Pop_PH.png', dpi=100, bbox_inches = "tight")
        return fig
     
    
    # Function that plots the total population as a function of time   
    def plot_Ptot(self):
        fig = plt.figure()
        plt.plot(self.t, self.totalpop.evaluate(self.t), color='black', label='true')
        plt.plot(self.t, self.Ptot, label='approx.')
        plt.xlabel('Time [yr]')
        plt.ylabel('Total population [10³ indiv.]')
        plt.legend(loc ='upper left')
        fig.savefig('outputs/Totalpop_PH.png', dpi=100, bbox_inches = "tight")
        return fig
        
    
    # Function that plots the number of women in their fertility period with time
    def plot_Pw(self):
        fig = plt.figure()
        plt.plot(self.t, self.women)
        plt.xlabel('Time [yr]')
        plt.ylabel('Number of fertile women [10³ indiv.]')
        fig.savefig('outputs/PopW_PH.png', dpi=100, bbox_inches = "tight")
        return fig
       
    
    # Function that plots the numerical approximation and the UN data
    def plot_comparison(self, ind): 
        fig = plt.figure()
        plt.plot(self.a, self.pop.evaluate(self.a, ind), color='black', label='true')
        plt.plot(self.a, self.P[:, ind], color='red', label='approx.')
        plt.xlabel('Age [yr]')
        plt.ylabel('Population repartition in ' + str(self.t0+ind) + ' [10³ indiv.]')
        plt.legend(loc ='upper right') 
        fig.savefig('outputs/Pop_' + str(ind) + '_PH.png', dpi=100, bbox_inches = "tight")
        return fig
        
        