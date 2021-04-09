#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 14:56:45 2021

@author: maxmhuggins
"""

import backtester as bt
import datareader as dr
import matplotlib.pyplot as plt


class ExampleStrategy:

    def __init__(self, closes, dates, symbol):

        self.Closes, self.Dates, self.Symbol = closes, dates, symbol

        self.StartingBalance = 10000000
        self.N = 2
        self.StrategyName = ('Drop Twice, Buy,'
                             + 'Jump Thrice, Sell (Example)')

        self.BackTester = bt.BackTester(self.Closes,
                                        self.Dates,
                                        self.StartingBalance,
                                        self.strategy,
                                        symbol=self.Symbol,
                                        strategy_name=self.StrategyName,
                                        path='../figures/')

    def strategy(self):
        optimizing_parameter = self.N

        backtester = self.BackTester
        percent = .25
        counter = 0
        for i in range(2, len(self.Closes)):
            current_close = self.Closes[i]

            positions = backtester.NumberOfPositions

            if positions == 0:
                for previous_value in range(1, optimizing_parameter + 1):
                    if current_close < self.Closes[i-previous_value]:
                        counter += 1
                    else:
                        counter = 0
                if counter == optimizing_parameter:
                    backtester.buy(percent, i)

            elif positions > 0:
                for previous_value in range(1, 2*optimizing_parameter+1):
                    if current_close > self.Closes[i-previous_value]:
                        counter += 1
                    else:
                        counter = 0
                if counter == optimizing_parameter:
                    backtester.sell(i)


if __name__ == '__main__':
    start = '2021-03-02'
    end = '2021-04-09'
    symbol = 'DOGEUSDT'
    dates = (start, end)
    BTC = dr.DataReader(symbol, 'binance', dates, tick='1h')
    Strat = ExampleStrategy(BTC.Closes, BTC.Dates, symbol)
    # Strat.BackTester.runner()
    optimize_range = range(1, 10)
    for i in optimize_range:
        Strat.N = i
        Strat.BackTester.runner()

    plt.scatter(optimize_range, Strat.BackTester.Gains, marker='x')
    plt.plot(optimize_range, Strat.BackTester.Gains, lw=.5)
    Strat.BackTester.optimizer()
