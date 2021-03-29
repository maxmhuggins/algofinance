#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 06:01:25 2021

@author: maxmhuggins

Example for making a good looking figure.
"""


import datareader as dr
import variations as vr
import matplotlib.pyplot as plt
import time
import numpy as np

plt.style.use('classic')
size = 20
size_config = .8
legendfont = 10
thickness = 1.5
color_value = '#6b8ba4'

start = '2021-03-02'
end = '2021-03-05'
dates = (start, end)
BTC = dr.DataReader('BTCUSDT', 'binance', dates, '1m')
BTCVariations = vr.Variations(BTC.Dates, BTC.Closes, normalized=True)

STORJ = dr.DataReader('STORJUSDT', 'binance', dates, '1m')
STORJVariations = vr.Variations(STORJ.Dates, STORJ.Closes, normalized=True)

ETH = dr.DataReader('ETHUSDT', 'binance', dates, '1m')
ETHVariations = vr.Variations(ETH.Dates, ETH.Closes, normalized=True)


PandemicStartTime = (time.mktime(time.strptime('01/21/2020', '%m/%d/%Y')))

PanX = np.linspace(PandemicStartTime, PandemicStartTime)
PanY = np.linspace(.9*min(BTC.Closes), 1.1*max(BTC.Closes))


fig = plt.figure(1, figsize=(12, 6))
plt.plot(BTC.Dates, BTC.Closes, color='black', label='BTCUSDT', linewidth=.2)
plt.plot(PanX, PanY, label='First COVID-19 Case in US', alpha=.5,
         linestyle=':', color='magenta')
plt.xlabel('Time (seconds since epoch)')
plt.ylabel('Closing Prices')
plt.xlim(BTC.Dates[0], BTC.Dates[-1])
plt.ylim(.9*min(BTC.Closes), 1.1*max(BTC.Closes))
plt.title('Closing Prices for BTCUSDT From {} to {}'.format(start, end))
plt.legend(loc='best')
plt.savefig('./figures/BTCExamplePlot.png', dpi=600)

fig = plt.figure(2, figsize=(12, 6))
plt.plot(STORJ.Dates, STORJ.Closes, color='black', label='STORJUSDT', linewidth=.2)
plt.plot(PanX, PanY, label='First COVID-19 Case in US', alpha=.5,
         linestyle=':', color='magenta')
plt.xlabel('Time (seconds since epoch)')
plt.ylabel('Closing Prices')
plt.xlim(STORJ.Dates[0], STORJ.Dates[-1])
plt.ylim(.9*min(STORJ.Closes), 1.1*max(STORJ.Closes))
plt.title('Closing Prices for STORJUSDT From {} to {}'.format(start, end))
plt.legend(loc='best')
plt.savefig('./figures/STORJExamplePlot.png', dpi=600)

fig = plt.figure(3, figsize=(12, 6))
plt.plot(ETH.Dates, ETH.Closes, color='black', label='ETHUSDT', linewidth=.2)
plt.plot(PanX, PanY, label='First COVID-19 Case in US', alpha=.5,
         linestyle=':', color='magenta')
plt.xlabel('Time (seconds since epoch)')
plt.ylabel('Closing Prices')
plt.xlim(ETH.Dates[0], ETH.Dates[-1])
plt.ylim(.9*min(ETH.Closes), 1.1*max(ETH.Closes))
plt.title('Closing Prices for ETHUSDT From {} to {}'.format(start, end))
plt.legend(loc='best')
plt.savefig('./figures/ETHExamplePlot.png', dpi=600)

fig = plt.figure(4, figsize=(24, 6))
fig.suptitle('Variations', fontsize=size)
plt.subplot(131)
plt.ylabel('Normalized Variation', fontsize=size_config*size)
plt.xlabel('Time')
plt.bar(BTCVariations.Dates, BTCVariations.Variations, label='BTCUSDT')
plt.xlim(BTCVariations.Dates[0], BTCVariations.Dates[-1])
plt.legend(loc='best', fontsize=legendfont)
#=================================================#
plt.subplot(132)
plt.ylabel('Normalized Variation', fontsize=size_config*size)
plt.xlabel('Time')
plt.bar(STORJVariations.Dates, STORJVariations.Variations, label='STORJUSDT', color='b')
plt.xlim(STORJVariations.Dates[0], STORJVariations.Dates[-1])
plt.legend(loc='best', fontsize=legendfont)
#=================================================#
plt.subplot(133)
plt.ylabel('Normalized Variation', fontsize=size_config*size)
plt.xlabel('Time')
plt.bar(ETHVariations.Dates, ETHVariations.Variations, label='ETHUSDT', color='m')
plt.xlim(ETHVariations.Dates[0], ETHVariations.Dates[-1])
plt.legend(loc='best', fontsize=legendfont)
#=================================================#
plt.savefig('./figures/VariationsExamplePlot.png', dpi=600)
