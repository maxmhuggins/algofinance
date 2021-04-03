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
# ========================================================================== #
plt.style.use('classic')
size = 20
size_config = .8
legendfont = 10
thickness = 0.3
width = .5
resolution = 300
color_value = '#6b8ba4'
# ========================================================================== #
start = '2020-04-03'
end = '2021-04-03'
dates = (start, end)
BTC = dr.DataReader('BTCUSDT', 'binance', dates, '1d')
BTCVariations = vr.Variations(BTC.Dates, BTC.Closes, normalized=True)

STORJ = dr.DataReader('STORJUSDT', 'binance', dates, '1d')
STORJVariations = vr.Variations(STORJ.Dates, STORJ.Closes, normalized=True)

ETH = dr.DataReader('ETHUSDT', 'binance', dates, '1d')
ETHVariations = vr.Variations(ETH.Dates, ETH.Closes, normalized=True)
# ========================================================================== #
max_variations = [max(BTCVariations.Variations),
                  max(ETHVariations.Variations),
                  max(STORJVariations.Variations)]

min_variations = [min(BTCVariations.Variations),
                  min(ETHVariations.Variations),
                  min(STORJVariations.Variations)]

max_closes = [max(BTCVariations.ShiftedCloses),
              max(STORJVariations.ShiftedCloses),
              max(ETHVariations.ShiftedCloses)]

min_closes = [min(BTCVariations.ShiftedCloses),
              min(STORJVariations.ShiftedCloses),
              min(ETHVariations.ShiftedCloses)]

abs_max_closes = 0.9 * max([max(max_closes),
                            abs(min(min_closes))])

abs_max_variations = 1.1 * max([max(max_variations),
                                abs(min(min_variations))])

PandemicStartTime = (time.mktime(time.strptime('2020-01-21', '%Y-%m-%d')))

PanX = np.linspace(PandemicStartTime - BTC.Dates[0],
                   PandemicStartTime - BTC.Dates[0])
PanY = np.linspace(.9*min(min_closes),
                   1.1*max(max_closes))
# ========================================================================== #
fig = plt.figure(1, figsize=(12, 6))

plt.plot(BTCVariations.ShiftedDates, BTCVariations.ShiftedCloses,
         color=color_value, label='BTCUSDT', linewidth=width)

plt.plot(PanX, PanY, label='First COVID-19 Case in US', alpha=.5,
         linestyle=':', color='black')

plt.xlabel('Time (s)')
plt.ylabel('Closing Prices')
plt.xlim(BTCVariations.ShiftedDates[0], BTCVariations.ShiftedDates[-1])

plt.ylim(.9*min(BTCVariations.ShiftedCloses),
         1.1*max(BTCVariations.ShiftedCloses))

plt.title('Closing Prices for BTCUSDT From {} to {}'.format(start, end))
plt.legend(loc='best')
plt.savefig('./figures/BTCExamplePlot.png', dpi=resolution)
# ========================================================================== #
fig = plt.figure(2, figsize=(12, 6))

plt.plot(STORJVariations.ShiftedDates, STORJVariations.ShiftedCloses,
         color=color_value, label='STORJUSDT', linewidth=width)

plt.plot(PanX, PanY, label='First COVID-19 Case in US', alpha=.5,
         linestyle=':', color='magenta')

plt.xlabel('Time (s)')
plt.ylabel('Closing Prices')
plt.xlim(STORJVariations.ShiftedDates[0], STORJVariations.ShiftedDates[-1])

plt.ylim(.9*min(STORJVariations.ShiftedCloses),
         1.1*max(STORJVariations.ShiftedCloses))

plt.title('Closing Prices for STORJUSDT From {} to {}'.format(start, end))
plt.legend(loc='best')
plt.savefig('./figures/STORJExamplePlot.png', dpi=resolution)
# ========================================================================== #
fig = plt.figure(3, figsize=(12, 6))

plt.plot(ETHVariations.ShiftedDates, ETHVariations.ShiftedCloses,
         color=color_value, label='ETHUSDT', linewidth=width)

plt.plot(PanX, PanY, label='First COVID-19 Case in US', alpha=.5,
         linestyle=':', color='magenta')

plt.xlabel('Time (s)')
plt.ylabel('Closing Prices')
plt.xlim(ETHVariations.ShiftedDates[0], ETHVariations.ShiftedDates[-1])

plt.ylim(.9*min(ETHVariations.ShiftedCloses),
         1.1*max(ETHVariations.ShiftedCloses))

plt.title('Closing Prices for ETHUSDT From {} to {}'.format(start, end))
plt.legend(loc='best')
plt.savefig('./figures/ETHExamplePlot.png', dpi=resolution)
# ========================================================================== #
fig = plt.figure(4, figsize=(24, 6))
fig.suptitle('Variations', fontsize=size)
plt.subplot(131)
plt.ylabel('Normalized Variation', fontsize=size_config*size)
plt.xlabel('Time (s)')

plt.plot(BTCVariations.Dates, BTCVariations.Variations, label='BTCUSDT',
         color='black', lw=thickness)

plt.xlim(BTCVariations.Dates[0], BTCVariations.Dates[-1])
plt.ylim(-abs_max_variations, abs_max_variations)
plt.legend(loc='best', fontsize=legendfont)
# ========================================================================== #
plt.subplot(132)
plt.ylabel('Normalized Variation', fontsize=size_config*size)
plt.xlabel('Time (s)')

plt.plot(STORJVariations.Dates, STORJVariations.Variations, label='STORJUSDT',
         color='b', lw=thickness)

plt.xlim(STORJVariations.Dates[0], STORJVariations.Dates[-1])
plt.ylim(-abs_max_variations, abs_max_variations)
plt.legend(loc='best', fontsize=legendfont)
# ========================================================================== #
plt.subplot(133)
plt.ylabel('Normalized Variation', fontsize=size_config*size)
plt.xlabel('Time (s)')

plt.plot(ETHVariations.Dates, ETHVariations.Variations, label='ETHUSDT',
         color='m', lw=thickness)

plt.xlim(ETHVariations.Dates[0], ETHVariations.Dates[-1])
plt.ylim(-abs_max_variations, abs_max_variations)
plt.legend(loc='best', fontsize=legendfont)
plt.savefig('./figures/VariationsExamplePlot.png', dpi=resolution)
# ========================================================================== #
print('Negative Variations for STORJ: %.2f' % STORJVariations.NegativeVariations)
print('Positive Variations for STORJ: %.2f' % STORJVariations.PositiveVariations)
print('Total Variations for STORJ: %.2f' % STORJVariations.TotalVariations)

