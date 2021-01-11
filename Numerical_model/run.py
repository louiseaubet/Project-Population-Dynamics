# -*- coding: utf-8 -*-
"""Run file"""

from main import *

####################################
# Parameters set by the user 

location = 'Philippines'  # 
ti = 1950
tf = 2020 

h = 1. # length of time interval

A = 100  # maximum age 
t0 = 1950    # beginning of the simulation

###################################

main(location, ti, tf, t0, h, A)