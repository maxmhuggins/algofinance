#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 07:45:55 2021

@author: maxmhuggins
"""

import matplotlib.pyplot as plt
plt.style.use('classic')


class BackTester:

    def __init__(self, closes, dates, starting_balance, strategy, symbol):

        self.Closes = closes
        self.Dates = dates
        self.StartingBalance = starting_balance
        self.Position = None
        self.Symbol = symbol
        self.ColorValue = '#6b8ba4'
        self.Width = .5

        self.Buys, self.Sells = [], []

        self.strategy = strategy

    def buy(self, close):
        self.Buys.append(close)
        self.Position = True

    def sell(self, close):
        self.Sells.append(close)
        self.Position = None

    def broker(self):
        buy_sum = 0
        sell_sum = 0

        for i in range(0, len(self.Buys)):
            buy_sum += self.Buys[i]
            self.BuyIndex.append(self.) # NEED TO MAKE A BUY AND SELL INDEX FOR PLOTTING
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

    def make_plot(self, path='./Figures'):
        fig = plt.figure(1, figsize=(12, 6))

        plt.plot(self.Dates, self.Closes, color=self.ColorValue,
                 label=self.Symbol, linewidth=self.Width)
        
        plt.scatter(self.BuyIndex, self.Buys, label='First COVID-19 Case in US', alpha=.5,
                 linestyle=':', color='magenta')
        
        plt.xlabel('Time (s)')
        plt.ylabel('Closing Prices')
        plt.xlim(STORJVariations.ShiftedDates[0], STORJVariations.ShiftedDates[-1])
        
        plt.ylim(.9*min(STORJVariations.ShiftedCloses),
                 1.1*max(STORJVariations.ShiftedCloses))
        
        plt.title('Closing Prices for STORJUSDT From {} to {}'.format(start, end))
        plt.legend(loc='best')
        plt.savefig('./figures/STORJExamplePlot.png', dpi=resolution)
                