#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 08:10:57 2021

@author: maxmhuggins
"""

"""
This will provide an example strategy. It will take in a set of closes and
dates, run the strategy and then output a set of buys and sells
"""

import backtester as bt


class ExampleStrategy:

    def __init__(self, closes, dates):
        self.Closes = closes
        self.Dates = dates
        
        self.Buys, self.Sells = [], []
        
    def moving_average(self, start, end):
        timespan = range(start, end)
        summer = 0

        for i in timespan:
            summer += self.Closes[i]
        average = summer / len(timespan)
        
        return average
    
    def Buy(self, close):
        self.Buys.append(close)

    def strategy(self):
        for i in range(0, len(self.Closes)):
            average = self.moving_average(0, i)
            if self.Closes[i] < average:
                self.Buy(close)