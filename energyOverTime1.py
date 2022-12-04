# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 14:13:30 2022

@author: Deant
"""

'''
COMPUTE AND MODEL BITCOIN MINING AS THERMODYNAMIC CARNOT SYSTEM OVER TIME
'''

'IMPORTING NECESSARY LIBRARIES'

import numpy as np
import json as js
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
import scipy.interpolate as interp

'SETTING GLOBAL CONSTANTS'

sigma = 1.3806*10**-23 #Boltzmann constant
Tc = 25+273 #Temperature cold in Kelvin
Th = 75+273 #Temperature hot in Kelvin
Win = 270 #Work in J/s
bph = 256 #Bits per has
T = Th-Tc

s_b = 600 #seconds to get the block every 10 minutes
s_d = 86400 #seconds in a day

'READING HASH RATE DATA'
#The file containing hash rate data over time representing the difficulty
f = open('hashRate.json')
hashRateData = js.load(f)['hash-rate'] #Hash rate info in TH/s
f.close()

#Convert from TeraHash/second to Hash/second
hashRate = [point['y']*10**12 for point in hashRateData]
#Convert each timestamp to a datetime object
x0 = [dt.datetime.fromtimestamp(int(point['x']*10**-3)) for point in hashRateData]

'CALCULATING WORK OUT'

#Calculate Work out from governing equation 
Wout = [sigma*T*np.log(2)*bph*hr*s_b for hr in hashRate]
#Gives rate of work in units of Joules/Block

'READING RATE OF WORK INPUT DATA'
gwpd = []
x1 = []
with open('powerInPerDay.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        x1.append(row[0])
        gwpd.append(row[4])

#Convert each timestamp to a datetime object
x1 = [dt.datetime.fromtimestamp(int(x)) for x in x1[2:]]

#Converting rate of work in into Joules/Block
Win = [float(g)*10**9/s_d*s_b for g in gwpd[2:]] #GWatts/day to jouls/block

'FIND EFFICIENCIES'





'PLOTTING THE DATA'

fig, ax1 = plt.subplots()

font1 = {'family':'serif','color':'blue','size':8}
font2 = {'family':'serif','color':'darkred','size':8}

plt.title('Joules of Work to Mine 1 Block Every 10 Minutes Over Time', fontdict = font1)

ax1.set_xlabel('Date', fontdict = font2)
ax1.set_ylabel('Joules of Work Out per Bitcoin Mined', fontdict = font2)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

ax1.plot_date(x0, Wout, marker = None, linestyle ='solid', color='red', label='Work Out', linewidth = 1)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('Joules of Work In per Bitcoin Mined', fontdict = font2)
ax2.plot_date(x1, Win, marker = None, linestyle ='solid', color='blue', label='Work In', linewidth = 1)

fig.legend(loc=(0.2, 0.73))

plt.gcf().autofmt_xdate()

plt.tight_layout()

plt.savefig('workvtime1.png', dpi=1200, bbox_inches="tight")
