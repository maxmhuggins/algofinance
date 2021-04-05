#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 08:10:57 2021

@author: maxmhuggins
"""


import backtester as bt
import datareader as dr


class ExampleStrategy:

    def __init__(self, closes, dates, symbol):
        self.Closes = closes
        self.Dates = dates
        self.Symbol = symbol

        self.StartingBalance = 10000000

        self.BackTester = bt.BackTester(self.Closes,
                                        self.Dates,
                                        self.StartingBalance,
                                        self.strategy,
                                        self.Symbol)

    def moving_average(self, start, end):
        timespan = range(start, end)
        summer = 0

        if len(timespan) == 0:
            average = 0
        else:
            for i in timespan:
                summer += self.Closes[i]
            average = summer / len(timespan)

        return average

    def strategy(self):
        backtester = self.BackTester
        for i in range(0, len(self.Closes)):
            average = self.moving_average(0, i)
            close = self.Closes[i]

            if backtester.Position is None:
                if close < average:
                    backtester.buy(close)
                else:
                    pass

            elif backtester.Position is not None:
                if close > average:
                    backtester.sell(close)


if __name__ == '__main__':
    start = '2020-03-02'
    end = '2021-03-05'
    symbol = 'BTCUSDT'
    dates = (start, end)
    BTC = dr.DataReader(symbol, 'binance', dates, tick='1d', timeunit='1d')
    Strat = ExampleStrategy(BTC.Closes, BTC.Dates, symbol)
    Strat.BackTester.get_results()
