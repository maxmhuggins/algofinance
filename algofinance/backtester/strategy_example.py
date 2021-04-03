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
import datareader as dr


class ExampleStrategy(bt.BackTester):

    def __init__(self, closes, dates):
        super().__init__(self)
        self.Closes = closes
        self.Dates = dates

    def moving_average(self, start, end):
        timespan = range(start, end)
        summer = 0

        for i in timespan:
            summer += self.Closes[i]
        average = summer / len(timespan)
        
        return average
    
    def strategy(self):
        for i in range(0, len(self.Closes)):
            average = self.moving_average(0, i)
            close = self.Closes[i]

            if self.Position is None:
                if close < average:
                    self.buy(close)
                else:
                    pass
            
            elif self.Position is not None:
                if close > average:
                    self.sell(close)

if __name__ == '__main__':
    start = '2020-03-02'
    end = '2021-03-05'
    dates = (start, end)
    BTC = dr.DataReader('BTCUSDT', 'binance', dates, tick='1d', timeunit='1d')
    Strat = ExampleStrategy(BTC.Closes, BTC.Dates)
    Strat.main()
    print(Strat.Buys, Strat.Sells)
                