#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 09:17:38 2021

@author: maxmhuggins
"""

import matplotlib.pyplot as plt

PV_i = 640
k = .25

time = range(0, 24)

PV = [PV_i]

for i in range(0, len(time)-1):
    PV.append(PV[i-1]*k+PV[i-1])

plt.plot(time, PV)

print('Final value: %.2f' % PV[-1])
