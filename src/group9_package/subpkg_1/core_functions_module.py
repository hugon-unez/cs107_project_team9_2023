#!/usr/bin/env python3
# File       : core_functions_module.py
# Description: Core functions module for spectral data analysis
# License    : GNU General Public License, version 3
# Copyright 2023 Harvard University. All Rights Reserved.

from astroquery.sdss import SDSS
from astropy.table import Table

class SpectralAnalysisBase:
    def __init__(self, query, data=None):
        self.query = query

        # check that data is same type as query
        if data is not None and not isinstance(data, Table):
            raise ValueError("data must be an Astropy Table object")
        
        self.data = data
