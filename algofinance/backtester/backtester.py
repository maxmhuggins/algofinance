#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 07:45:55 2021

@author: maxmhuggins
"""


class BackTester:

    def __init__(self, closes, dates, account_value, strategy):

        self.Closes = closes
        self.Dates = dates
        self.AccoutValue = account_value
        self.Position = None

        self.Buys, self.Sells = [], []

        self.Strategy = strategy

        self.Total = self.broker()

    def buy(self, close):
        self.Buys.append(close)
        self.Position = True

    def sell(self, close):
        self.Sells.append(close)
        self.Position = False

    def broker(self):
        buy_sum = 0
        sell_sum = 0
        for i in range(0, len(self.Buys)):
            buy_sum += self.Buys[i]
        for i in range(0, len(self.Sells)):
            sell_sum += self.Sells[i]

        return sell_sum - buy_sum

    def main(self):
        self.Strategy()
        return self.Buys, self.Sells
