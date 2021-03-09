#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 20:32:36 2021

@author: maxmhuggins

The class Variations takes in two numpy arrays and determines the tick to tick
variations in close data. It has options to determine the regular variations
or the "normalized" (so-to-speak) variations. Use the DataReader class to
gather data for analysis
"""

import numpy as np
import datareader as dr
import matplotlib.pyplot as plt


class Variations:

    def __init__(self, dates, closes, normalized=None):
        self.Dates = dates
        self.Closes = closes
        self.Normalized = normalized

        self.Dates, self.Variations = self.main()

    def absolute_variations(self):
        variations = []
        dates = self.Dates
        closes = self.Closes

        for i in range(0, len(dates)):
            if i == len(dates)-1:
                variations.append(np.nan)
            else:
                diff = closes[i] - closes[i+1]
                variations.append(diff)

        return dates, variations

    def shifter(self):
        shifted_dates = []
        shifted_closes = []

        for i in range(0, len(self.Dates)):
            shifted_closes.append(self.Closes[i]-self.Closes[0])
            shifted_dates.append(self.Dates[i]-self.Dates[0])

        return shifted_dates, shifted_closes

    def normalizer(self):
        shifted_dates, shifted_closes = self.shifter()

        normal_closes = []

        for i in range(0, len(shifted_dates)):
            new_normal_value = shifted_closes[i] / self.Closes[i]
            normal_closes.append(new_normal_value)

        return shifted_dates, normal_closes

    def normalized_variations(self):
        normal_dates, normal_closes = self.normalizer()

        normal_variations = []

        for i in range(0, len(normal_dates)):
            if i == len(normal_dates)-1:
                normal_variations.append(np.nan)
            else:
                variation = (normal_closes[i] - normal_closes[i+1]) \
                    / normal_closes[i]
                normal_variations.append(variation)

        return normal_dates, normal_variations

    def main(self):

        if self.Normalized is None:
            return self.absolute_variations()

        else:
            return self.normalized_variations()


start = '2021-02-02'
end = '2021-03-05'
dates = (start, end)
BTC = dr.DataReader('BTCUSDT', 'binance', dates, '1d')

dates, closes = BTC.Dates, BTC.Closes

BTCVariations = Variations(dates, closes, normalized=True)

# plt.plot(BTCVariations.Dates, BTCVariations.Closes)
print(BTCVariations.Closes)

"""
Need way to grab the from shifted lists for plotting, but don't
want to have to run the function twice to get them
"""
