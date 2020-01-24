#!/usr/bin/env python2
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

#temperature range of the 2 phase dome (280 to 99%Tcrit)
tempTwoPhaseDome = np.linspace(280, Tcrit*0.9999, 100, endpoint=True)

#range of saturated liquid values in dome based off two phase dome
entropySaturatedLiquid = PropsSI('S','T', tempTwoPhaseDome, 'Q', 0.0, material)
#range of saturated vapor values in dome
entropySaturatedVapor = PropsSI('S','T', tempTwoPhaseDome, 'Q', 1.0, material)

#pressure levels
PressureLevels = np.array([6e6, 6.6e6, 8e6, 8.8e6, 11e6, 14.8e6, 23e6])

#Enthalpy Levels
EnthalpyLevels = np.array([0.8, 0.9, 1.01, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0])
for i in range(len(EnthalpyLevels)):
    EnthalpyLevels[i] = EnthalpyLevels[i]*(Hcrit)


matplotlib.rcParams['lines.linewidth'] = 2
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.size'] = 40
matplotlib.rcParams['figure.figsize'] = 16, 12

#combine the two halves of the dome entropy values
entropyValues = np.concatenate((entropySaturatedLiquid,entropySaturatedVapor), axis=0)

#plot each half of the dome
plt.plot(entropySaturatedLiquid*1e-3, tempTwoPhaseDome,  'k-.',label='_nolegend_')
plt.plot(entropySaturatedVapor*1e-3, tempTwoPhaseDome,  'k--',label='_nolegend_')


entropyValues = np.linspace(1,2.7,num = 100)*1e3
#plot each isobar
for pressure in PressureLevels:
    tempValues = PropsSI('T','P',pressure, 'S', entropyValues, material)
    plt.scatter(entropyValues*1e-3, tempValues, label='Pressures', color = 'red')
    #next line didnt look good
    #plt.text(entropyValues[entropyValues.size-1]*1e-3, tempValues[tempValues.size-1], str(pressure*1e-6))

#plot each enthalpy line on separate axis
for enthalpy in EnthalpyLevels:
    tempValues = PropsSI('T','H',enthalpy, 'S', entropyValues, material)
    plt.scatter(entropyValues*1e-3, tempValues, label='Enthalpies',color = 'green')
    
plt.xlim([1,2.7])
plt.ylim([290, 800])
plt.xlabel('Specific Entropy(kJ/K/kg)')
plt.ylabel('Temperature (K)')
plt.title('T-S Diagram for CO2')
 
plt.savefig('problem1.pdf')   
plt.savefig('problem1.jpg')   
plt.show()