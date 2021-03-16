#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 06:01:25 2021

@author: maxmhuggins

Example for making a good looking figure.
"""


import datareader as dr
import matplotlib.pyplot as plt
import time
import numpy as np

start = '2020-01-02'
end = '2021-03-05'
dates = (start, end)
BTC = dr.DataReader('BTCUSDT', 'binance', dates, '1d')


PandemicStartTime = (time.mktime(time.strptime('01/21/2020', '%m/%d/%Y')))

PanX = np.linspace(PandemicStartTime, PandemicStartTime)
PanY = np.linspace(.9*min(BTC.Closes), 1.1*max(BTC.Closes))


fig = plt.figure(1, figsize=(12, 6))
plt.plot(BTC.Dates, BTC.Closes, color='black', label='BTCUSDT', linewidth=.2)
plt.plot(PanX, PanY, label='First COVID-19 Case in US', alpha=.5,
         linestyle=':', color='magenta')
plt.xlabel('Time (days)')
plt.ylabel('Closing Prices')
plt.xlim(BTC.Dates[0], BTC.Dates[-1])
plt.ylim(.9*min(BTC.Closes), 1.1*max(BTC.Closes))
plt.title('Closing Prices for BTCUSDT From {} to {}'.format(start, end))
plt.legend(loc='best')
plt.savefig('./figures/ExamplePlot.png', dpi=600)
