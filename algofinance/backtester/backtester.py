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
                 strategy_name):

        self.Closes = closes
        self.Dates = dates
        self.StartingBalance = starting_balance
        self.AccountValue = starting_balance
        self.NumberOfPositions = 0
        self.Commission = 1 - .01

        self.Symbol = symbol
        self.StrategyName = strategy_name
        self.ColorValue = '#6b8ba4'
        self.Resolution = 300
        self.Width = .5

        self.Buys, self.Sells, self.BuyIndex, self.SellIndex = [], [], [], []

        self.strategy = strategy

    def buy(self, percent, index):
        self.Buys.append(self.Closes[index])
        self.BuyIndex.append(self.Dates[index])

        self.NumberOfPositions = (self.NumberOfPositions
                                  + (percent * self.AccountValue)
                                  / self.Closes[index])

        self.AccountValue = self.Commission * (self.AccountValue
                                               - (self.NumberOfPositions
                                                  * self.Closes[index]))

    def sell(self, percent, index):
        self.Sells.append(self.Closes[index])
        self.SellIndex.append(self.Dates[index])

        self.AccountValue = self.Commission * (self.AccountValue
                                               + (self.NumberOfPositions
                                                  * self.Closes[index]))

        self.NumberOfPositions = 0

    def lines(self):
        """ I want to implement a function that looks at differences between a
        buy and a sell order and determines if it was profitable, then plot
        some kind of indicator to visualize the gain/loss"""
        for i in range(0, self.Buys):
            pass

    def broker(self):
        """ I don't need the broker method right now, but I believe I will in
        the future so it is just a placeholder right now"""
        pass

    def optimizer(self, parameters, ranges):
        """I want to implement tensor flow to optimize strategies but for now
        I'm going to settle with some dinky brute force methods"""
        # for i in range(0,len(parameters)):
        #     parameter = parameter[i]

        #     for l in range(0, len(self.Closes)):

    def get_results(self):
        self.strategy()
        self.FinalBalance = self.AccountValue
        self.Gain = (100 * self.AccountValue / self.StartingBalance) - 100
        print('Your starting balance: %.0f' % self.StartingBalance)
        print('Your final balance: %.5f' % self.AccountValue)
        print('Percent Gain: %.5f' % self.Gain)

    def make_plot(self, indicator, path='./figures',
                  plot_name='ExamplePlot.png'):

        plt.figure(figsize=(12, 6))
        for i in range(0, len(indicator)):
            indicator[i]()
        plt.plot(self.Dates, self.Closes, color=self.ColorValue,
                 label=self.Symbol, linewidth=self.Width)

        plt.scatter(self.BuyIndex, self.Buys, label='buys', alpha=.5,
                    color='red')
        plt.scatter(self.SellIndex, self.Sells, label='sells', alpha=.5,
                    color='green')

        plt.xlabel('Time (s)')
        plt.ylabel('Prices')
        plt.xlim(self.Dates[0], self.Dates[-1])
        plt.ylim(.9*min(self.Closes), 1.1*max(self.Closes))

        plt.title('{}'.format(self.StrategyName))
        plt.legend(loc='best')
        plt.savefig(path + plot_name, dpi=self.Resolution)
