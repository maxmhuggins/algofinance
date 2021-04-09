#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 06:08:57 2021

@author: maxmhuggins

This script will be meant to visualize the crypto market and how it is doing.
It will iterate through a list of all of the available cryptos, plot their
closes and then it will also take an average of all of the crypto markets and
plot that w.r.t. time to visualize the health of the market. Maybe it should
also look at variations, not sure yet.
"""


import numpy as np
import matplotlib.pyplot as plt
import datareader as dr

coins = []

columns = np.loadtxt('./data/list_of_cryptos', delimiter=',', skiprows=1,
                     dtype='str')

for column in columns:
    coins.append(column[0])

start = '2021-01-02'
end = '2021-03-05'
dates = (start, end)
BTC = dr.DataReader('BTCUSDT', 'binance', dates, tick='1d')

for coin in coins:
    current_coin = dr.DataReader('{}USDT'.format(coin), 'binance', dates,
                                 tick='1d')
    plt.plot(current_coin.Dates, current_coin.Closes, label=coin)
    plt.legend(loc='best')
    plt.show()
