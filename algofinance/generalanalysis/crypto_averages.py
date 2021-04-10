#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 06:08:57 2021

@author: maxmhuggins

This can now grab all the coins stored in a text file, normalize them using
the variations module, then plot them seperately. What I would like to do is
join all of the datasets into a single "average" of them all. I may use
pandas join() function to do this.
"""


import numpy as np
import matplotlib.pyplot as plt
import datareader as dr
import variations as vr
color_value = '#6b8ba4'


class CryptoAverages:

    def __init__(self):
        self.CoinSymbols = []
        self.Start = '2020-10-10'
        self.End = '2021-04-10'  # Make this a today thing
        self.Dates = (self.Start, self.End)

    def grab_coin_symbols(self):
        columns = np.loadtxt('./data/list_of_cryptos', delimiter=',',
                             skiprows=1, dtype='str')
        for column in columns:
            self.CoinSymbols.append(column[0])

    def get_data(self, symbol):
        coin_data = dr.DataReader('{}USDT'.format(symbol), 'binance',
                                  self.Dates, tick='1d')
        data = (coin_data.Dates, coin_data.Closes)

        return data

    def make_normal(self, symbol):
        dates, closes = self.get_data(symbol)
        data_variations = vr.Variations(dates, closes, normalized=True)
        normalized_data = (data_variations.ShiftedDates,
                           data_variations.ShiftedCloses)

        return normalized_data

    def make_plot(self):
        average_closes = np.zeros(1)
        number_of_coins = len(self.CoinSymbols)
        maxes, mins = [], []
        plt.figure(figsize=(12, 6))

        for coin in self.CoinSymbols:
            dates, closes = self.make_normal(coin)
            maxes.append(max(closes))
            mins.append(min(closes))
            average_closes = average_closes + np.array(closes)

            plt.plot(dates, closes, color='black', lw=.5, alpha=.3)

        average_closes = average_closes / number_of_coins
        plt.plot(dates, average_closes, color='m', label='Average')
        plt.title('"Health" of the Crypto Market')
        plt.xlabel('TIme (s)')
        plt.ylabel('Gain')
        plt.xlim(dates[0], dates[-1])
        plt.ylim(.9*min(mins), 1.1*max(maxes))
        plt.legend(loc='best')
        plt.savefig('./figures/MarketHealth.png')

        print('Market Average Gain:', average_closes[-1])

    def main(self):
        self.grab_coin_symbols()
        self.make_plot()


test = CryptoAverages()
test.main()
