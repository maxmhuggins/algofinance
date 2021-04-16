#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 20:32:36 2021

The variations module is a data analysis tool that is able to produce both
"normalized" data sets as well as all of the variations between closing data
in a market.

@author: maxmhuggins
"""

from numpy import nan


class Variations:
    """
    Looks at the variations between market closes and normalizes data.

    Attributes
    ----------
    Dates : numpy.ndarray
        Numpy array of time data, typically gathered from datareader
    Closes : numpy.ndarray
        Numpy array of closing data, typically gathered from datareader
    Normalized : bool
        Tells Variations whether or not to "normalize" the data
    GainedCloses : list
        List of gains calculated from closing data.
    ShiftedDates : list
        Shifted to start from zero time data
    ShiftedCloses
        "Normalized" and shifted to start from zero closing data
    NegativeVariations : list
        List of all of the negative swinging variations for a data set
    PositiveVariations : lsit
        List of all of the positive swinging variations for a data set
    TotalVariations : list
        List of all of the variations for a data set

    Notes
    -----
    You may find quotation marks around anything labelled as normal. This is
    because I am using the term liberally here. All of the "normalization" that
    is done, is not really normalization but rather tools for making better
    comparisons between data sets.

    """

    def __init__(self, dates, closes, normalized=False):
        """
        Initializes the Variations class and makes several attributes.

        Parameters
        ----------
        dates : numpy.ndarray
            Array of time data, typically obtained from datareader
        closes : numpy.ndarray
            Array of closing data, typically obtained from datareader
        normalized : bool, optional
            Tells Variations whether or not to return normalized data. The
            default is False.

        Returns
        -------
        None.

        """
        self.Dates = dates
        self.Closes = closes
        self.Normalized = normalized

        self.GainedCloses = self.calculate_gains()
        self.ShiftedDates, self.ShiftedCloses = self.normalizer()

        self.Dates, self.Variations = self.main()
        (self.NegativeVariations, self.PositiveVariations,
         self.TotalVariations) = self.psuedo_volatility()

    def absolute_variations(self):
        """
        Calculates the variations in Closes using Dates as an index.

        Returns
        -------
        dates : list
            List of time data made from Dates.
        variations : list
            List of variations between each closing data point.

        Notes
        -----
        Iterates through the closing data and looks at the difference between
        two neighboring points. It is important that the difference is
        calcualted by subtracting the next point from the current point rather
        than the other way around. This establishes a correct sign for whether
        or not the price varied positively or negatively.

        """
        variations = []
        dates = self.Dates
        closes = self.Closes

        for i in range(0, len(dates)):
            if i == len(dates)-1:
                variations.append(nan)
            else:
                diff = closes[i] - closes[i+1]
                variations.append(diff)

        return dates, variations

    def normalizer(self):
        """
        Shifts data such that it is starting from zero.

        Returns
        -------
        shifted_dates : list
            Time data shifted so it starts from zero rather than the beginning
            of UNIX.
        shifted_closes : list
            Closing data shifted so it starts from zero rather than the price
            at the beginning of the interval.

        Notes
        -----
        Shifts data by computing the difference between each point in the set
        and the first point.

        """
        shifted_dates, shifted_closes = [], []

        for i in range(0, len(self.Dates)):
            shifted_closes.append(
                self.GainedCloses[i]-self.GainedCloses[0])

            shifted_dates.append(
                self.Dates[i]-self.Dates[0])

        return shifted_dates, shifted_closes

    def calculate_gains(self):
        """
        Computes gain of each closing point in the data set, relative to first.

        Returns
        -------
        normalized_closes : list
            List of gains calculated from the closing data.

        Notes
        -----
        Calculates the gain of a set of closing data by dividing each point in
        the set by the first point and subtracting one.

        """
        normalized_closes = []

        for i in range(0, len(self.Closes)):
            normalized_close = self.Closes[i]/self.Closes[0] - 1
            normalized_closes.append(normalized_close)

        return normalized_closes

    def normalized_variations(self):
        """
        Calculates "normalized" variations for a set of closing data

        Returns
        -------
        dates : list
            Time data.
        normal_variations : list
            List of "normalized" variations.

        Notes
        -----
        Calculates the "normal" variations by subtracting the next close from
        the current one, then dividing the result by the current close. The
        idea here is to look at the percent change in the price so a
        comparison can be made to another set of closing data. Who cares if the
        price of a coin changed x dollars if it is only .0001 percent of the
        price of the coin at that time.

        Again, quotations around normal because this isn't really a
        normalization, but rather a tool to make fairer comparisons.

        """
        dates, closes = self.Dates, self.Closes

        normal_variations = []

        for i in range(0, len(dates)):
            if i == len(dates)-1:
                normal_variations.append(nan)
            else:
                variation = (closes[i] - closes[i+1])\
                    / closes[i]
                normal_variations.append(variation)

        return dates, normal_variations

    def psuedo_volatility(self):
        """
        Calculates the amount of variations that a set of data will see.

        Returns
        -------
        negative_summer : float
            Summation of all of the negative variation swings for a set of
            variations data.
        positive_summer : float
            Summation of all of the positive variation swings for a set of
            variations data.
        total_variations : float
            Summation of all of the variation swings for a set of variations
            data.

        """
        variations = self.Variations

        negative_summer = 0
        positive_summer = 0

        for i in range(0, len(variations)):
            if variations[i] < 0:
                negative_variation = variations[i]
                negative_summer += negative_variation

            if variations[i] > 0:
                positive_variation = variations[i]
                positive_summer += positive_variation

        total_variations = abs(negative_summer) + positive_summer

        return negative_summer, positive_summer, total_variations

    def main(self):

        if self.Normalized is False:
            return self.absolute_variations()

        else:
            return self.normalized_variations()
