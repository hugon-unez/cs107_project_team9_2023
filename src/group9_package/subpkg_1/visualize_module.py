#!/usr/bin/env python3
# File       : visualize_module.py
# Description: Visualization module for spectral analysis
# License    : GNU General Public License, version 3
# Copyright 2023 Harvard University. All Rights Reserved.


import matplotlib
import pandas as pd
import numpy as np
from core_functions_module_extract import SpectraExtract
from astropy.table import Table

class SpectralVisualizer:
    def __init__(self, *, row=None, data=None):
        if (row is not None and not isinstance(row, Table.Row)) or (data is not None and not isinstance(data, pd.DataFrame)):
            raise TypeError("Invalid type for parameter. 'row' should be Table.Row or 'data' should be a pandas DataFrame.")


        if (row is not None and data is not None) or (row is None and data is None):
            raise ValueError("Either 'row' or 'data' should be provided, but not both or neither.")


        self.row = row
        self.data = data if data is not None else pd.DataFrame()  # Initialize data attribute
