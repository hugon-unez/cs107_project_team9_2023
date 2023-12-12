#!/usr/bin/env python3
# File       : visualize_module.py
# Description: Visualization module for spectral analysis
# License    : GNU General Public License, version 3
# Copyright 2023 Harvard University. All Rights Reserved.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from group9_package.subpkg_1.core_functions_module_extract import SpectraExtract
from astropy.table import Table



class SpectralVisualizer:
    def __init__(self, *, row=None, data=None):
        if (row is not None and not isinstance(row, Table.Row)) or (data is not None and not isinstance(data, pd.DataFrame)):
            raise TypeError("Invalid type for parameter. 'row' should be Table.Row or 'data' should be a pandas DataFrame.")

        if (row is not None and data is not None) or (row is None and data is None):
            raise ValueError("Either 'row' or 'data' should be provided, but not both or neither.")

        self.row = row
        self.data = data if data is not None else pd.DataFrame()  # Initialize data attribute

    def visualize(self):
        if self.data.empty and self.row is not None:
            spectra_extractor = SpectraExtract(self.row)
            self.data = spectra_extractor.extract_spectra()

        if self.data is None:
            raise ValueError("Both 'data' and 'row' are None or empty. Provide either 'data' or 'row' with valid data.")


        # Assuming 'Wavelength' and 'Flux' are column names in the DataFrame
        x = self.data['Wavelength']
        y = self.data['Flux']

        plt.figure()

        plt.plot(x, y)
        plt.xlabel('Wavelength')
        plt.ylabel('Flux')
        plt.title('Spectral Visualization')
        plt.show()
