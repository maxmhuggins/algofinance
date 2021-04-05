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

        self.NumberOfPositions = (self.NumberOfPositions # ** This needs work. The point is to get rid of this funky idea of a single position being held at a time
                                  + (percent * self.AccountValue)
                                  / self.Closes[index])

        self.AccountValue = (self.AccountValue
                             - (self.NumberOfPositions * self.Closes[index]))
        print('buy', self.AccountValue)

    def sell(self, percent, index):
        self.Sells.append(self.Closes[index])
        self.SellIndex.append(self.Dates[index])

        self.NumberOfPositions = (self.NumberOfPositions
                                  - (percent * self.AccountValue)
                                  / self.Closes[index])

        self.AccountValue = (self.AccountValue
                             + (self.NumberOfPositions * self.Closes[index]))
        print('sell', self.AccountValue)

    def broker(self):
        buy_sum = 0
        sell_sum = 0

        for i in range(0, len(self.Buys)):
            buy_sum += self.Buys[i]
        for i in range(0, len(self.Sells)):
            sell_sum += self.Sells[i]

        final_balance = self.StartingBalance - (sell_sum - buy_sum)
        gain = ((final_balance / self.StartingBalance) * 100) - 100

        return final_balance, gain

    def get_results(self):
        self.strategy()
        self.FinalBalance, self.Gain = self.broker()
        print('Your starting balance: %.0f' % self.StartingBalance)
        print('Your final balance: %.5f' % self.FinalBalance)
        print('Percent Gain: %.5f' % self.Gain)
        self.make_plot()

    def make_plot(self, path='./Figures', plot_name='ExamplePlot.png'):
        plt.figure(figsize=(12, 6))

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
