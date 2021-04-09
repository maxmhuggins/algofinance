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
import matplotlib.pyplot as plt
plt.style.use('classic')


class Variations:

    def __init__(self, dates, closes, normalized=None):
        self.Dates = dates
        self.Closes = closes
        self.Normalized = normalized

        self.NormalizedCloses = self.normalizer()
        self.ShiftedDates, self.ShiftedCloses = self.shifter()

        self.Dates, self.Variations = self.main()
        (self.NegativeVariations, self.PositiveVariations,
         self.TotalVariations) = self.psuedo_volatility()

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
        shifted_dates, shifted_closes = [], []

        for i in range(0, len(self.Dates)):
            shifted_closes.append(
                self.NormalizedCloses[i]-self.NormalizedCloses[0])

            shifted_dates.append(
                self.Dates[i]-self.Dates[0])

        return shifted_dates, shifted_closes

    def normalizer(self):
        normalized_closes = []

        for i in range(0, len(self.Closes)):
            if i == 0:
                normalized_closes.append(0)
            else:
                normalized_close = self.Closes[i]/self.Closes[0]
                normalized_closes.append(normalized_close)

        return normalized_closes

    def normalized_variations(self):
        dates, closes = self.Dates, self.Closes

        normal_variations = []

        for i in range(0, len(dates)):
            if i == len(dates)-1:
                normal_variations.append(np.nan)
            else:
                variation = (closes[i+1] - closes[i])\
                    / closes[i]
                normal_variations.append(variation)

        return dates, normal_variations

    def psuedo_volatility(self):
        variations = self.Variations

        negative_summer = 0
        positive_summer = 0

        for i in range(0, len(variations)):
            if variations[i] < 0:
                negative_variation = variations[i]
                negative_summer += negative_variation

            if variations[i] > 0:
                positive_variation = variations[i]
                positive_summer += positive_variation

        total_variations = abs(negative_summer) + positive_summer

        return negative_summer, positive_summer, total_variations

    def main(self):

        if self.Normalized is None:
            return self.absolute_variations()

        else:
            return self.normalized_variations()


"""
Need way to grab the from shifted lists for plotting, but don't
want to have to run the function twice to get them
    Maybe this should just be a seperate class?
"""
