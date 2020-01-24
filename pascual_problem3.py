3#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:49:24 2017

@author: nandopas
"""


import CoolProp.CoolProp as CP
from CoolProp.CoolProp import PropsSI
import numpy as np
import scipy as sci
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
#from pylab import figure, plot, xlabel, grid, hold, legend, title, savefig
from pylab import *
from scipy.optimize import curve_fit

material = 'CO2'

#calculate critical values
Tcrit = PropsSI('Tcrit', material)
Pcrit = PropsSI('Pcrit', material)
Scrit = PropsSI('S','T',Tcrit,'P',Pcrit,material)
Hcrit = PropsSI('H','T',Tcrit,'P',Pcrit,material)

print('Critical Temperature: ' + str(round(Tcrit,3)) + ' K')
print('Critical Pressure: ' + str(round(Pcrit*1e-6,3)) + ' MPa')
print('Critical Specific Entropy: ' + str(round(Scrit*1e-3,3)) + ' kJ/K/kg')
print('Critical Specific Enthalpy: ' + str(round(Hcrit*1e-3,3)) + ' kJ/kg')

PHigh = 23*1e6
PLow = 6.6*1e6
efficiency = 0.9


#states
'''
      P     T   h   s
1|  6.6    
2|  23
3|  23
4|  23     750
5|  6.6
6|  6.6

state 1 is saturated liquid
'''
#Pressures
P1 = 6.6*1e6
P2 = 23*1e6
P3 = 23*1e6
P4 = 23*1e6
P5 = 6.6*1e6
P6 = 6.6*1e6
#Temperatures
T1 = 0
T2 = 0
T3 = 0
T  = 0
T5 = 0
T6 = 0

#Specific Enthalpies
H1 = 0 #Done
H2 = 0
H3 = 0
H4 = 0
H5 = 0
H6 = 0
#Specific Entropies
S1 = 0 #S1 = S2
S2 = 0
S3 = 0
S4 = 0 #S4 = S5
S5 = 0
S6 = 0


#HRVG Properties
material_exhaust = 'air'
T_in = 811.15
T_out = 553.15
m_exhaust = 69.8 #kg/s'
P_atm = 101325 #Pa
H_in = PropsSI('H','P',P_atm,'T',T_in,material_exhaust)
H_out = PropsSI('H','P',P_atm,'T',T_out,material_exhaust)

Powers = []
ms = []

for T4 in range(350,781,10):
    
    #State4
    H4 = PropsSI('H','P',P4,'T',T4,material)
    S4 = PropsSI('S','P',P4,'T',T4,material)
    
    #State5
    S5 = S4
    H5s = PropsSI('H','P',P5,'S',S5,material)
    H5 = H4 - (0.8*(H4-H5s))
    T5 = PropsSI('T','P',P5,'H',H5,material)
    
    #state 1
    H1 = PropsSI('H','P',P1,'Q',0,material)
    S1 = PropsSI('S','P',P1,'Q',0,material)
    T1 = PropsSI('T','P',P1,'Q',0,material)
        
    #State2
    S2 = S1
    H2s = PropsSI('H','P',P2,'S',S2,material)
    H2 = H1+((H2s-H1)/0.85)
    T2 = PropsSI('T','P',P2,'H',H2,material)
    
    #State6
    #eta = (T5-T6)/(T5-T2)
    T6 = T5 - (efficiency*(T5-T2))
    H6 = PropsSI('H','P',P6,'T',T6,material)
    S6 = PropsSI('S','P',P6,'T',T6,material)
    
    #State3
    #Use energy balance equation for a regenerator
    #where there is no heat transfer or work done
    #and mass flow rates are all equivalent
    #we determine 0 = (h5+h2)-(h6+h3)
    H3 = (H5+H2)-H6
    T3 = PropsSI('T','P',P3,'H',H3,material)
    S3 = PropsSI('S','P',P3,'H',H3,material)
    
    #mass flow rate of working fluid
    #Use energy balance equation with the HRVG as the control volume
    #solve for m
    m = m_exhaust*((H_in-H_out)/(H4-H3))
    #Specific work of turbine
    Work_turbine = H4-H5
    #Specific work of pump
    Work_pump = H2-H1
    #Heat supplied per kg
    Heat_supplied = H4-H3

    #checking heat transfer boundary conditions
    if T5-T3 <= 10 or T6-T2 <= 10:
        continue
    if T3 > 523:
        continue
        
    #Net power
    Power = m*((H4-H5)-(H2-H1))
    Powers.append(Power*1e-3)
    ms.append(m)
    
    
    
matplotlib.rcParams['lines.linewidth'] = 2
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.size'] = 40
matplotlib.rcParams['figure.figsize'] = 16, 12

plt.plot(ms,Powers)
#plt.ylim([0, 6000])
#plt.xlim([50,120])
plt.xlabel('Mass Flow Rate - Working Fluid (kg/s)')
plt.ylabel('Net Power Output (kW)')
plt.title('Power Output with Varying Mass Flow Rate')
plt.savefig('problem3.pdf')   
plt.savefig('problem3.jpg')   
plt.show()