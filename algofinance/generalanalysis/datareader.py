#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 20:16:04 2021

The datareader module gathers market data, times and closes, from a specified
source and returns it in the form of a tuple containing two numpy arrays.

@author: maxmhuggins
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

    Attributes
    ----------
    Symbol : str
        Ticker symbol from respective source.
    Source : str
        Place where data is sourced. Can be either 'yahoo' or 'binance'.
    Tick : str
        Resolution of the acquired data.
    DateRange : tuple
        The range of dates the data will span. In the form:
            (YYYY-MM-DD, YYYY-MM-DD)
        start and end respectively.
    TimeFormat : str
        String format for dates.
    APIKey : str
        Key provided by Binance for collecting data.
    APISecret : str
        Secret key specific to a user on Binance for collecting data.
    BClient : class 'binance.client.Client'
        Binance's API for accessing their data

    """

    def __init__(self, symbol, source, daterange, tick='1d'):
        """
        Initializes the DataReader class and runs the main() method.

        Parameters
        ----------
        symbol : str
            Ticker symbol from respective source.
        source : str
            Place where data is sourced. Can be either 'yahoo' or 'binance'.
        daterange : tuple
            The range of dates the data will span. In the form:
                ('YYYY-MM-DD', 'YYYY-MM-DD')
            start and end respectively.
        tick : str, optional
            Resolution of the acquired data. The default is '1d'.

        Returns
        -------
        None.

        """
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
        tuple
            Tuple containing time and closing data as numpy arrays for
            specified range.

        """

        start = time.strptime('{}'.format(self.DateRange[0]), self.TimeFormat)
        end = time.strptime('{}'.format(self.DateRange[1]), self.TimeFormat)
        # start and end are made into struct_times

        start = time.mktime(start)
        end = time.mktime(end) + (TimeUnits[self.Tick])
        # yfinance ends 1 tick early while gathering data, so add 1 tick here
        # Convert to floats representing time in seconds

        start = time.strftime(self.TimeFormat, time.gmtime(start))
        end = time.strftime(self.TimeFormat, time.gmtime(end))
        # Convert into usable strings for yfinance

        data = yf.download(self.Symbol, start=start, end=end)
        # Data is gathered from Yahoo Finance

        data = data.reset_index()
        closes = data[TimeFormats[self.Source]['Close']].values.tolist()
        dates = data[TimeFormats[self.Source]['Timestamp']].values.tolist()
        dates = [dates[date]/1e9 for date in range(0, len(dates))]  # ns to s
        # Data gets made into useful format for my purposes

        return np.array(dates), np.array(closes)

    def binance_extractor(self):
        """
        Gathers market data from Binance using provided APIKeys.

        Returns
        -------
        tuple
            Tuple containing time and closing data as numpy arrays for
            specified range.

        """

        start = time.strptime('{}'.format(self.DateRange[0]), self.TimeFormat)
        end = time.strptime('{}'.format(self.DateRange[1]), self.TimeFormat)
        # start and end are made into struct_times

        start = time.mktime(start)
        end = time.mktime(end)
        # Convert to floats representing time in seconds

        start = time.strftime(self.TimeFormat, time.gmtime(start))
        end = time.strftime(self.TimeFormat, time.gmtime(end))
        # Convert into usable strings for Binance

        klines = self.BClient.get_historical_klines(self.Symbol,
                                                    self.Tick,
                                                    start, end, 1000)
        # Data is gathered from Binance

        data = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av',
            'ignore'])
        data = data.reset_index()
        closes = data[TimeFormats[self.Source]['Close']].values.tolist()
        closes = [float(closes[close]) for close in range(0, len(closes))]
        dates = data[TimeFormats[self.Source]['Timestamp']].values.tolist()
        dates = [dates[date]/1e3 for date in range(0, len(dates))]  # ms to s
        # Data gets made into useful format for my purposes

        return np.array(dates), np.array(closes)

    def csv(self):
        # TODO: would optionally like to be able to save a simple csv for
        # running large data sets.
        pass

    def main(self):
        """
        Decides to source data from Yahoo or Binance.

        Returns
        -------
        None.

        """
        if self.Source == 'yahoo':
            self.Dates, self.Closes = self.yahoo_extractor()
        if self.Source == 'binance':
            self.Dates, self.Closes = self.binance_extractor()
