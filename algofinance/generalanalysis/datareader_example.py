#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 18:13:55 2021

@author: maxmhuggins

This is an example of the proper usage for the datareader.py file
"""

import generalanalysis


def main():
    dr = generalanalysis.datareader

    start = '2021-02-02'
    end = '2021-03-05'
    dates = (start, end)
    BTC = dr.DataReader('BTCUSDT', 'binance', dates, '1d')
    TSLA = dr.DataReader('TSLA', 'yahoo', dates, '1d')
    print('BTC:', BTC.Dates, '\n', 'TSLA:', TSLA.Dates)


if __name__ == '__main__':
    main()
