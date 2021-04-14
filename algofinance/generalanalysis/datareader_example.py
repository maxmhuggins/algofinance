#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 18:13:55 2021

This is an example of the proper usage for the datareader module.

@author: maxmhuggins

"""

import datareader as dr


def main():

    start = '2021-03-02'
    end = '2021-03-05'
    dates = (start, end)
    BTC = dr.DataReader('BTCUSDT', 'binance', dates, tick='1d')
    TSLA = dr.DataReader('TSLA', 'yahoo', dates)
    print('BTC:', BTC.Dates, '\n', 'TSLA:', TSLA.Dates)


if __name__ == '__main__':
    main()
