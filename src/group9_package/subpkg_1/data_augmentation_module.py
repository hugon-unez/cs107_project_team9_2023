#!/usr/bin/env python3
# File       : data_augmentation_module.py
# Description: Data Augmentation Module for Spectral Data Analysis Derivatives
# License    : GNU General Public License, version 3
# Copyright 2023 Harvard University. All Rights Reserved.

from astroquery.sdss import SDSS
import numpy as np
import pandas as pd
import differint.differint as df

class DataAugmentation:
    """A Class for Augmenting Preprocessed Spectral data with derivatives and fractional derivatives"""
    def __init__(self, data):
        """Initializes DataAugmentation Class

        Args:
            data (Pandas Data Frame, optional): data to compute derivatives on

        Raises:
            ValueError: If the given data is not an astropy table
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError('Data is not a Pandas Data Frame')
        self.data = data

    def compute_derivative(self, column_name):
        """Computes the Derivative of a column for spectral data and creates a
        column with the derivative data

        Args:
            data (Pandas Data Frame): spectral data to compute derivatives on
            column_name: the name of the column to compite the derivative on

        Raises:
            ValueError: If the given column is not a column in the data
        """
        if column_name not in self.data.columns.tolist():
            raise ValueError('Column is not in the Preprocessed Spectral Data')
        self.data[f'{column_name} Derivative'] = np.gradient(self.data[column_name], axis=0)
        return self.data

    def compute_fractional_derivative(self, column_name, derivative_order):
        """Computes the Fractional Derivative of a column for spectral data and
        creates a column with the derivative data

        Args:
            data (Pandas Data Frame): spectral data to compute derivatives on
            column_name: the name of the column to compite the derivative on
            derivative_order: the order of the derivative to take

        Raises:
            ValueError: If the given column is not a column in the data
        """
        if column_name not in self.data.columns.tolist():
            raise ValueError('Column is not in the Preprocessed Spectral Data')
        frac_diff = df.GLI(derivative_order, self.data[column_name].ravel(),num_points=self.data[column_name].shape[0])
        self.data[f'{column_name}_fractional_derivative'] = frac_diff
        return self.data

    def augment_both_derivatives(self, column_name, derivative_order):
        """Computes the Regular and Fractional Derivative of a column for
        spectral data and creates a column with the derivative data

        Args:
            data (Pandas Data Frame): spectral data to compute derivatives on
            column_name: the name of the column to compite the derivative on
            derivative_order: the order of the derivative to take
        """
        self.compute_derivative(column_name)
        self.compute_fractional_derivative(column_name, derivative_order)
        return self.data