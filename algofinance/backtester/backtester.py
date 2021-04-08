#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 07:45:55 2021

@author: maxmhuggins
"""

import matplotlib.pyplot as plt
plt.style.use('classic')


class BackTester:

    def __init__(self, closes, dates, starting_balance, strategy, symbol,
                 strategy_name, indicators=None, plot=True):

        self.Closes = closes
        self.Dates = dates
        self.StartingBalance = starting_balance
        self.Strategy = strategy
        self.AccountValue = starting_balance
        self.Indicators = indicators
        self.Plot = plot
        self.NumberOfPositions = 0
        self.Commission = 1 - .01

        self.Symbol = symbol
        self.StrategyName = strategy_name
        self.ColorValue = '#6b8ba4'
        self.Resolution = 300
        self.Width = .5

        (self.Buys, self.Sells, self.BuyIndex, self.SellIndex,
         self.PositionValuesAtBuy, self.PositionValuesAtSell,
         self.Gains) = ([], [], [], [], [], [], [])

    def buy(self, percent, index):
        close = self.Closes[index]
        date = self.Dates[index]
        self.Buys.append(close)
        self.BuyIndex.append(date)

        self.NumberOfPositions = (self.NumberOfPositions
                                  + (percent * self.AccountValue)
                                  / close)

        position_value = self.NumberOfPositions * close
        self.PositionValuesAtBuy.append(position_value)

        self.AccountValue = self.Commission * (self.AccountValue
                                               - (self.NumberOfPositions
                                                  * close))

    def sell(self, index):
        close = self.Closes[index]
        date = self.Dates[index]
        self.Sells.append(close)
        self.SellIndex.append(date)

        self.AccountValue = self.Commission * (self.AccountValue
                                               + (self.NumberOfPositions
                                                  * close))

        position_value = self.NumberOfPositions * close
        self.PositionValuesAtSell.append(position_value)
        self.NumberOfPositions = 0

    def lines(self):
        for i in range(0, len(self.PositionValuesAtSell)):
            sell_value = self.PositionValuesAtSell[i]
            buy_value = self.PositionValuesAtBuy[i]
            difference = sell_value - buy_value
            width = 1.25

            dates = [self.BuyIndex[i], self.SellIndex[i]]
            closes = [self.Buys[i], self.Sells[i]]
            if difference > 0:
                plt.plot(dates, closes, color='green', linewidth=width)
            elif difference == 0:
                plt.plot(dates, closes, color='black', linewidth=width)
            elif difference < 0:
                plt.plot(dates, closes, color='red', linewidth=width)

    def broker(self):
        """ I don't need the broker method right now, but I believe I will in
        the future so it is just a placeholder right now"""
        pass

    # def optimizer(self, optimizing_parameter, optimize_range):
    #     """I want to implement tensor flow to optimize strategies but for now
    #     I'm going to settle with some dinky brute force methods"""
    #     for i in optimize_range:
    #         self.Gains.append(self.runner(optimizing_parameter))

    #     plt.scatter(optimize_range, self.Gains)

    def make_plot(self, path='./figures/',
                  plot_name='ExamplePlot.png'):

        plt.figure(figsize=(12, 6))

        if self.Indicators is None:
            pass

        else:
            for i in range(0, len(self.Indicators)):
                self.Indicators[i]()

        plt.plot(self.Dates, self.Closes, color=self.ColorValue,
                 label=self.Symbol, linewidth=self.Width)

        plt.scatter(self.BuyIndex, self.Buys, label='buys', alpha=.5,
                    color='red')

        plt.scatter(self.SellIndex, self.Sells, label='sells', alpha=.5,
                    color='green')

        self.lines()

        plt.xlabel('Time (s)')
        plt.ylabel('Prices')
        plt.xlim(self.Dates[0], self.Dates[-1])
        plt.ylim(.9*min(self.Closes), 1.1*max(self.Closes))
        plt.title('{}'.format(self.StrategyName))
        plt.legend(loc='best')
        plt.savefig(path + plot_name, dpi=self.Resolution)

    def get_results(self):
        print('Your starting balance: %.0f' % self.StartingBalance)
        print('Your final balance: %.5f' % self.AccountValue)
        print('Percent Gain: %.5f' % self.Gain)
        if self.Plot is False:
            pass
        else:
            self.make_plot()

    def runner(self):
        self.Strategy()
        if self.NumberOfPositions > 0:
            self.sell(len(self.Closes)-1)
        self.FinalBalance = self.AccountValue
        self.Gain = (100 * self.AccountValue / self.StartingBalance) - 100
        self.Gains.append(self.Gain)
        self.get_results()
