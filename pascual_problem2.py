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
T4 = 750
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

#state 1
H1 = PropsSI('H','P',P1,'Q',0,material)
S1 = PropsSI('S','P',P1,'Q',0,material)
T1 = PropsSI('T','P',P1,'Q',0,material)

#State4
H4 = PropsSI('H','P',P4,'T',T4,material)
S4 = PropsSI('S','P',P4,'T',T4,material)

#State5
S5 = S4
H5 = PropsSI('H','P',P5,'S',S5,material)
T5 = PropsSI('T','P',P5,'H',H5,material)

#State2
S2 = S1
H2 = PropsSI('H','P',P2,'S',S2,material)
T2 = PropsSI('T','P',P2,'S',S2,material)

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

#temperature range of the 2 phase dome (280 to 99%Tcrit)
tempTwoPhaseDome = np.linspace(280, Tcrit*0.9999, 100, endpoint=True)

#range of saturated liquid values in dome based off two phase dome
entropySaturatedLiquid = PropsSI('S','T', tempTwoPhaseDome, 'Q', 0.0, material)
#range of saturated vapor values in dome
entropySaturatedVapor = PropsSI('S','T', tempTwoPhaseDome, 'Q', 1.0, material)

#pressure levels
PressureLevels = np.array([6.6e6, 23e6])

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
plt.plot(entropySaturatedLiquid*1e-3, tempTwoPhaseDome,  'k-.',label='sat liq')
plt.plot(entropySaturatedVapor*1e-3, tempTwoPhaseDome,  'k--',label='sat vap')

entropyValues = np.linspace(1,2.7,num = 100)*1e3
#plot each isobar
for pressure in PressureLevels:
    tempValues = PropsSI('T','P',pressure, 'S', entropyValues, material)
    plt.scatter(entropyValues*1e-3, tempValues, label=str(pressure))
    plt.plot()
'''
#plot each enthalpy line on separate axis
for enthalpy in EnthalpyLevels:
    tempValues = PropsSI('T','H',enthalpy, 'S', entropyValues, material)
    ax2.scatter(entropyValues*1e-3, tempValues, label=str(enthalpy))
    '''
plt.ylim([290, 800])
plt.xlim([1,2.7])
plt.xlabel('Specific entropy (kJ/K/kg)')
plt.ylabel('Temperature (K)')
plt.title('S-CO2 Rankine Cycle with HRVG')

 
#plt.savefig('IsobarsOnTSdiagram.pdf')   
entropies = np.array([S1*1e-3,S2*1e-3,S3*1e-3,S4*1e-3,S5*1e-3,S6*1e-3])
temperatures = np.array([T1,T2,T3,T4,T5,T6])

plt.plot((entropies[0],entropies[1]),(temperatures[0],temperatures[1]),'.r-')
plt.plot((entropies[3],entropies[4]),(temperatures[3],temperatures[4]),'.r-')

#plot the states
plt.plot(S1*1e-3,T1,marker='o', markersize=6, color="red", label='state 1')
plt.plot(S2*1e-3,T2,marker='o', markersize=6, color="red", label='state 2')
plt.plot(S3*1e-3,T3,marker='o', markersize=6, color="red", label='state 3')
plt.plot(S4*1e-3,T4,marker='o', markersize=6, color="red", label='state 4')
plt.plot(S5*1e-3,T5,marker='o', markersize=6, color="red", label='state 5')
plt.plot(S6*1e-3,T6,marker='o', markersize=6, color="red", label='state 6')

#to show each state on the graph as text
for i in range(temperatures.size):
    text = 'State ' + str(i+1)
    plt.text(entropies[i],temperatures[i],text,fontsize = 20)
    
plt.savefig('problem2.pdf')   
plt.savefig('problem2.jpg')   
    
plt.show()

'''
specific work produced by the turbine
specific work consumed by the pump
heat supplied to the working fluid in the HRVG (per kg of CO 2 )
overall efficiency of the cycle
'''
#specific work of turbine
Work_turbine = H4-H5
#specific work of pump
Work_pump = H2-H1
#Heat supplied per kg
Heat_supplied = H4-H3
#Overall Efficiency
Cycle_efficiency = (Work_turbine-Work_pump)/Heat_supplied

#############reevaluating for an ideal rankine cycle#############
material = 'Water'

#State 1, temperature equal to HRVG cycle
Rankine_T1 = T1
Rankine_P1 = 6.6*1e6
Rankine_H1 = PropsSI('H','T',Rankine_T1,'Q',0,material)
Rankine_S1 = PropsSI('S','T',Rankine_T1,'Q',0,material)

#State 2
Rankine_S2 = Rankine_S1
Rankine_P2 = 20*1e6
Rankine_T2 = PropsSI('T','P',Rankine_P2,'S',Rankine_S2,material)
Rankine_H2 = PropsSI('H','P',Rankine_P2,'S',Rankine_S2,material)

#State 3
Rankine_P3 = 20*1e6
Rankine_T3 = 750
Rankine_H3 = PropsSI('H','P',Rankine_P3,'T',Rankine_T3,material)
Rankine_S3 = PropsSI('S','P',Rankine_P3,'T',Rankine_T3,material)

#State 4
Rankine_P4 = 6.6*1e6
Rankine_S4 = Rankine_S3
Rankine_H4 = PropsSI('H','P',Rankine_P4,'S',Rankine_S4,material)


Rankine_turbine = Rankine_H3-Rankine_H4
Rankine_pump = Rankine_H2 - Rankine_H1
Rankine_heat = Rankine_H3 - Rankine_H2
Rankine_efficiency = (Rankine_turbine - Rankine_pump)/Rankine_heat

print('S-CO2 efficiency: ' + str(round(Cycle_efficiency*100,2)) + '%')
print('Rankine efficiency: ' + str(round(Rankine_efficiency*100,2)) + '%')


