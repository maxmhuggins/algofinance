#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 05:45:50 2021

@author: maxmhuggins

This is an example of the proper usage for the Variations class
"""
import datareader as dr
import variations as vr
import matplotlib.pyplot as plt


def main():

    start = '2020-02-05'
    end = '2021-03-05'
    dates = (start, end)
    BTC = dr.DataReader('BTCUSDT', 'binance', dates, '1d')
    BTCVariations = vr.Variations(BTC.Dates, BTC.Closes, normalized=True)

    plt.bar(BTCVariations.Dates, BTCVariations.Variations)
    plt.xlim(BTCVariations.Dates[0], BTCVariations.Dates[-1])


if __name__ == '__main__':
    main()
