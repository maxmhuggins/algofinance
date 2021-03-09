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


class Variations:

    def __init__(self, dates, closes, normalized=None):
        self.Dates = dates
        self.Closes = closes
        self.Normalized = normalized

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
        return variations

    def normal_variations(self):
        normal_dates, normal_closes = self.normalizer()
# RUN NORMALIZED VARIATIONS ALGO

    def normalizer(self):
        normal_dates = []
        normal_closes = []

        for i in range(0, len(self.Dates)):
            normal_closes.append(self.Closes[i]-self.Closes[0])
            normal_dates.append(self.Dates[i]-self.Dates[0])

        return normal_dates, normal_closes

    def main(self):

        if self.Normalized is None:
            self.Variations = self.absolute_variations()

        else:
            self.Variations = self.normal_variations()
            # Need way to grab the from zero closes for plotting, but don't
            # want to have to run the function twice to get them