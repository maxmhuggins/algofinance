#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 20:16:04 2021

@author: maxmhuggins

The class DataReader serves the purpose to take an input of information,
specifically symbol, source, daterange, and ticker, and output two numpy
arrays of time and close data where time is in units of hours. The symbol
should be in the form listed by the source by which it is taken
(f.e. Tesla should be in the form TSLA for the
source yahoo. The source should be the name of the source, all lower case and
no spaces. The daterange should be in the form of a tuple with two values,
start and end. The date format being yyyy/mm/dd
f.e. February 26, 2019 to January 15, 2020 is represented by:
 (2019-02-26, 2020-01-15)

"""

import pandas as pd
from binance.client import Client
import yfinance as yf
import time
import numpy as np
from dictionaries import TimeUnits, TimeFormats
from APIKeys import APIKey, APISecret


class DataReader:
    """
    Extracts market data from binance and yahoo.

    ...

    Attributes
    ----------
    Symbol : str
        Ticker symbol from respective source.
    Source : str
        Place where data is sourced.
    Tick : str
        Resolution of the acquired data.
    DateRange : str
        The range of dates the data will span.
    TimeFormat : str
        String format for dates.
    APIKey : str
        Key provided by Binance for collecting data.
    APISecret : str
        Secret key specific to a user on Binance for collecting data.
    BClient : class
        Binance's API for accessing their data

    """

    def __init__(self, symbol, source, daterange, tick='1d'):

        self.Symbol = symbol
        self.Source = source
        self.Tick = tick
        self.DateRange = daterange
        self.TimeFormat = '%Y-%m-%d'
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.BClient = Client(api_key=self.APIKey, api_secret=self.APISecret)

        self.main()

    def yahoo_extractor(self):
        """
        Gathers market data from yahoo finance.

        Returns
        -------
        numpy.ndarray
            Time and closing data for specified range.

        """
        start = time.strptime('{}'.format(self.DateRange[0]), self.TimeFormat)
        end = time.strptime('{}'.format(self.DateRange[1]), self.TimeFormat)
        start = time.mktime(start)
        end = time.mktime(end) + (TimeUnits[self.Tick])

        start = time.strftime(self.TimeFormat, time.gmtime(start))
        end = time.strftime(self.TimeFormat, time.gmtime(end))

        data = yf.download(self.Symbol, start=start, end=end)
        data = data.reset_index()

        Closes = data[TimeFormats[self.Source]['Close']].values.tolist()
        Dates = data[TimeFormats[self.Source]['Timestamp']].values.tolist()
        Dates = [Dates[date]/1e9 for date in range(0, len(Dates))]

        return np.array(Dates), np.array(Closes)

    def binance_extractor(self):

        start = time.strptime('{}'.format(self.DateRange[0]), self.TimeFormat)
        end = time.strptime('{}'.format(self.DateRange[1]), self.TimeFormat)
        start = time.mktime(start)
        end = time.mktime(end)

        start = time.strftime(self.TimeFormat, time.gmtime(start))
        end = time.strftime(self.TimeFormat, time.gmtime(end))
        klines = self.BClient.get_historical_klines(self.Symbol,
                                                    self.Tick,
                                                    start, end, 1000)

        data = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av',
            'ignore'])

        data = data.reset_index()
        Closes = data[TimeFormats[self.Source]['Close']].values.tolist()
        Closes = [float(Closes[close]) for close in range(0, len(Closes))]
        Dates = data[TimeFormats[self.Source]['Timestamp']].values.tolist()
        Dates = [Dates[date]/1e3 for date in range(0, len(Dates))]

        return np.array(Dates), np.array(Closes)

    def main(self):
        if self.Source == 'yahoo':
            self.Dates, self.Closes = self.yahoo_extractor()
        if self.Source == 'binance':
            self.Dates, self.Closes = self.binance_extractor()


"""
- I would like a way to optionally save a csv file of the output

- Write documentation and comment out
"""
