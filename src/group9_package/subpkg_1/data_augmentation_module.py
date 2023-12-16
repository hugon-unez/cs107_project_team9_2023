#!/usr/bin/env python3
# File       : data_augmentation_module.py
# Description: Data Augmentation Module for Spectral Data Analysis Derivatives
# License    : GNU General Public License, version 3
# Copyright 2023 Harvard University. All Rights Reserved.

from astroquery.sdss import SDSS
import numpy as np
import pandas as pd
from group9_package.subpkg_1.core_functions_module_extract import SpectraExtract

class DataAugmentation(SpectraExtract):
    
    def __init__(self, query):
        self.query = query

    def compute_derivative(self):
        pass

    def compute_fractional_derivative(self):
        pass

    def append_derivative(self):
        pass

    def append_fractional_derivative(self):
        pass

    def augument_data(self):
        pass