#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 06:04:16 2021

@author: maxmhuggins
"""

TimeFormats = {
    'yahoo': {
        'Date': '%Y-%m-%d %H:%M:%S', 'Close': 'Close', 'Timestamp': 'Date'
        },
    'binance': {
        'Date': '%Y-%m-%d %H:%M:%S', 'Close': 'close', 'Timestamp': 'timestamp'
        }
    }

TimeUnits = {'1M': 60*60*24*7*30, '1w': 60*60*24*7, '3d': 60*60*24*3,
             '1d': 60*60*24, '12h': 60*60*12, '1h': 60*60, '1m': 60
             }
