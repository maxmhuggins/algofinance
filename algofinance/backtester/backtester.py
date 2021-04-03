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

        self.Strategy = strategy

    def broker(self):
        
        
"""
- BackTester should take in closes, dates, and a strategy. This will then be
run by the script to determine profit gain/loss as well as provide analytics
and visuals
"""