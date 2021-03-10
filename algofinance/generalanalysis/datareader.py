#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 20:16:04 2021

@author: max

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

TimeFormats = {
    'yahoo': {
        'Date': '%Y-%m-%d %H:%M:%S', 'Close': 'Close', 'Timestamp': 'Date'
        },
    'binance': {
        'Date': '%Y-%m-%d %H:%M:%S', 'Close': 'close', 'Timestamp': 'timestamp'
        }
    }
"""
    KLINE_INTERVAL_1MINUTE = '1m'
    KLINE_INTERVAL_3MINUTE = '3m'
    KLINE_INTERVAL_5MINUTE = '5m'
    KLINE_INTERVAL_15MINUTE = '15m'
    KLINE_INTERVAL_30MINUTE = '30m'
    KLINE_INTERVAL_1HOUR = '1h'
    KLINE_INTERVAL_2HOUR = '2h'
    KLINE_INTERVAL_4HOUR = '4h'
    KLINE_INTERVAL_6HOUR = '6h'
    KLINE_INTERVAL_8HOUR = '8h'
    KLINE_INTERVAL_12HOUR = '12h'
    KLINE_INTERVAL_1DAY = '1d'
    KLINE_INTERVAL_3DAY = '3d'
    KLINE_INTERVAL_1WEEK = '1w'
    KLINE_INTERVAL_1MONTH = '1M'
    """
TimeUnits = {'1M': 60*60*24*7*30, '1w': 60*60*24*7, '3d': 60*60*24*3,
             '1d': 60*60*24, '12h': 60*60*12, '1h': 60*60, '1m': 60
             }


class DataReader:

    def __init__(self, symbol, source, daterange, interval):

        self.Symbol = symbol
        self.Source = source
        self.Interval = interval
        self.DateRange = daterange
        self.TimeFormat = '%Y-%m-%d'
        self.APIKey = (***REMOVED***
***REMOVED***)
        self.APISecret = (***REMOVED***
***REMOVED***)
        self.BClient = Client(api_key=self.APIKey, api_secret=self.APISecret)

        self.main()

    def yahoo_extractor(self):
        start = time.strptime('{}'.format(self.DateRange[0]), self.TimeFormat)
        end = time.strptime('{}'.format(self.DateRange[1]), self.TimeFormat)
        start = time.mktime(start)
        end = time.mktime(end) + (TimeUnits[self.Interval])

        start = time.strftime(self.TimeFormat, time.gmtime(start))
        end = time.strftime(self.TimeFormat, time.gmtime(end))

        data = yf.download(self.Symbol, start=start, end=end)
        data = data.reset_index()

        Closes = data[TimeFormats[self.Source]['Close']].values.tolist()
        Dates = data[TimeFormats[self.Source]['Timestamp']].values.tolist()
        # Dates = [Dates[date]/1e12 for date in range(0, len(Dates))]

        return np.array(Dates), np.array(Closes)

    def binance_extractor(self):

        start = time.strptime('{}'.format(self.DateRange[0]), self.TimeFormat)
        # print(start)
        end = time.strptime('{}'.format(self.DateRange[1]), self.TimeFormat)
        start = time.mktime(start)
        # print(start)
        end = time.mktime(end)

        start = time.strftime(self.TimeFormat, time.gmtime(start))
        # print(start)
        end = time.strftime(self.TimeFormat, time.gmtime(end))
        klines = self.BClient.get_historical_klines(self.Symbol,
                                                    self.Interval,
                                                    start, end, 1000)

        data = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av',
            'ignore'])

        data = data.reset_index()
        Closes = data[TimeFormats[self.Source]['Close']].values.tolist()
        Closes = [float(Closes[close]) for close in range(0, len(Closes))]
        Dates = data[TimeFormats[self.Source]['Timestamp']].values.tolist()
        # Dates = [Dates[date]/1e6 for date in range(0, len(Dates))]

        return np.array(Dates), np.array(Closes)

    def main(self):
        if self.Source == 'yahoo':
            self.Dates, self.Closes = self.yahoo_extractor()
        if self.Source == 'binance':
            self.Dates, self.Closes = self.binance_extractor()


"""
- Fix the slowness and optimize a little

- Write documentation and comment out
"""
