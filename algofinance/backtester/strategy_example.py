#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 08:10:57 2021

@author: maxmhuggins
"""


import backtester as bt
import datareader as dr
import matplotlib.pyplot as plt


class ExampleStrategy:

    def __init__(self, closes, dates, symbol):
        self.Closes = closes
        self.Dates = dates
        self.Symbol = symbol

        self.MovingAverageValues = []
        self.N = 5
        self.StrategyName = ('Under Average Buyer,'
                             + 'Over Average Seller (Example)')

        self.StartingBalance = 10000000
        self.BackTester = bt.BackTester(self.Closes,
                                        self.Dates,
                                        self.StartingBalance,
                                        self.strategy,
                                        self.Symbol,
                                        self.StrategyName)

    def moving_average(self, start, end):
        timespan = range(start, end)
        summer = 0

        if any(element < 0 for element in timespan):
            average = 0
        else:
            for i in timespan:
                summer += self.Closes[i]
            average = summer / len(timespan)

        return average

    def strategy(self):
        backtester = self.BackTester
        percent = .25
        for i in range(0, len(self.Closes)):
            average = self.moving_average(i-self.N, i)
            self.MovingAverageValues.append(average)
            close = self.Closes[i]

            if backtester.NumberOfPositions <= 0:
                if close < average:
                    backtester.buy(percent, i)
                else:
                    pass

            elif backtester.NumberOfPositions > 0:
                if close > average:
                    backtester.sell(1, i)

    def indicator(self):
        backtester = self.BackTester
        plt.plot(backtester.Dates, self.MovingAverageValues,
                 color='magenta', label='Moving Average',
                 linewidth=backtester.Width)


if __name__ == '__main__':
    start = '2020-03-02'
    end = '2021-03-05'
    symbol = 'DOGEUSDT'
    dates = (start, end)
    BTC = dr.DataReader(symbol, 'binance', dates, tick='1d', timeunit='1d')
    Strat = ExampleStrategy(BTC.Closes, BTC.Dates, symbol)
    Strat.BackTester.get_results()
    list_of_indicators = [Strat.indicator]
    Strat.BackTester.make_plot(list_of_indicators)
