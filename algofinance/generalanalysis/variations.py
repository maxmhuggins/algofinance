#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 20:32:36 2021

@author: maxmhuggins

The class Variations takes in two numpy arrays and determines the tick to tick
variations in close data. It has options to determine the regular variations
or the "normalized" (so-to-speak) variations. Use the DataReader class to
gather data for analysis
"""


import generalanalysis

dr = generalanalysis.datareader

class Variations(dr):

    def __init__(self, dates, closes, normalized=None):
        super().__init__(self)
        self.Dates = dr.Dates