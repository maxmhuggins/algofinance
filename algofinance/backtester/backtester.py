#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 07:45:55 2021

@author: maxmhuggins
"""


class BackTester:

    def __init__(self, closes, dates, starting_balance, strategy):

        self.Closes = closes
        self.Dates = dates
        self.StartingBalance = starting_balance
        self.Position = None

        self.Buys, self.Sells = [], []

        self.Strategy = strategy

        self.FinalBalance, self.Gain = self.broker()

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
        for i in range(0, len(self.Sells)):
            sell_sum += self.Sells[i]

        final_balance = self.StartingBalance - (sell_sum - buy_sum)
        gain = ((final_balance / self.StartingBalance) * 100) - 100

        return final_balance, gain

    def get_results(self):
        self.Strategy()
        print('Your starting balance: %.2f' % self.StartingBalance)
        print('Your final balance: %.2f' % self.FinalBalance)
        print('Percent Gain: %.2f' % self.Gain)
