#!/usr/bin/env python3
# File       : core_functions_module_modify.py
# Description: Modifies Spectral Data 
# License    : GNU General Public License, version 3
# Copyright 2023 Harvard University. All Rights Reserved.
"""
This python module extends the functionality of the core_functions_module_extract 
by focusing on data preprocessing and modification techniques of spectral data.
"""

from astroquery.sdss import SDSS
from scipy.interpolate import interp1d
from scipy.stats import zscore
import numpy as np
import pandas as pd
from group9_package.subpkg_1.core_functions_module_extract import SpectralAnalysisBase


class DataPreprocessor(SpectralAnalysisBase):
    """A Class for preprocessing spectral data including normalization, outlier removal, interpolation, and redshift correction."""
    def __init__(self, query, data=None):
        """Initializes the DataPreprocessor class with a SQL query or pre-loaded data.

        Args:
            query (str): SQL query to retrieve data from the SDSS database.
            data (pandas.DataFrame, optional): Pre-loaded spectral data in a pandas DataFrame. 
                Defaults to None.

        Raises:
            ValueError: If the provided data is not a pandas DataFrame.
        """
        #Similar to pp6 in that we're turning the query into a pandas dataframe
        self.query = query

        if not isinstance(data, pd.DataFrame) and data is not None:
            raise ValueError("Input data must be a pandas DataFrame")

        if data is None:
            job = SDSS.query_sql(self.query)
            self.data = job.to_pandas()
        else:
            self.data = data

        self.column_headers = list(self.data.columns)

    def normalize_data(self):
        """Normalizes the spectral data using Z-score normalization.

        Raises:
            ValueError: If there is no data available for normalization.
        """
        if self.data is not None:
            # Perform normalization on the data 
            #looping through each column and normalizing each one and replacing them 
            for header in self.column_headers:
                normalized_flux_data = (self.data[header] - np.mean(self.data[header])) / np.std(self.data[header])
                #Resetting what the column is equal to
                self.data[header] = normalized_flux_data
        else:
            raise ValueError("No data available for normalization")

    def remove_outliers(self, threshold=2.5):
        """Removes outliers from the spectral data based on a Z-score threshold.

        Args:
            threshold (float, optional): The Z-score threshold for identifying outliers. 
                Defaults to 2.5.

        Raises:
            ValueError: If there is no data available for outlier removal.
        """
        if self.data is not None:
            for header in self.column_headers:
                # Remove outliers from data in using z-score
                z_scores = np.abs(zscore(self.data[header]))
                outliers_removed = self.data[header][z_scores < threshold]
                self.data[header] = outliers_removed
        else:
            raise ValueError("No data available for outlier removal")

    def interpolate_data(self, new_wavelengths):
        """Interpolates the spectral data to new wavelengths.

        Args:
            new_wavelengths (list or array): The new wavelengths for interpolation.

        Raises:
            ValueError: If there is insufficient data for interpolation or if the lengths of new and old wavelengths do not match.
        """
        if self.data is not None:
            if len(self.column_headers) < 2:
                raise ValueError("Insufficient columns in self.column_headers for interpolation")

            # Assume wavelength is at index 0 and flux is at index 1
            header_wavelength = self.column_headers[0]
            header_flux = self.column_headers[1]

            # Extract wavelengths and flux values
            old_wavelengths = self.data[header_wavelength]
            flux_values = self.data[header_flux]

            # Check if lengths match
            if len(new_wavelengths) != len(old_wavelengths):
                raise ValueError("Length of new_wavelengths does not match the length of old wavelengths")
            
            # Create interpolation function
            interp_function = interp1d(np.array(old_wavelengths.values), np.array(flux_values.values), kind='cubic', fill_value="extrapolate", bounds_error=False)

            # Use the interpolation function to estimate values at new_wavelengths
            interpolated_values = interp_function(new_wavelengths)

            # Update the dataframe with the interpolated values
            self.data[header_flux] = interpolated_values
        else:
            raise ValueError("No data available for interpolation")

    def correct_redshift(self, bands=['u', 'g', 'r', 'i']):
        """Corrects the wavelengths of spectral data for redshift.

        Args:
            bands (list of str, optional): List of bands to apply redshift correction. 
                Defaults to ['u', 'g', 'r', 'i'].

        Raises:
            ValueError: If there is no wavelength data available for redshift correction.
        """
        if self.data is not None:
            # Adjust wavelengths in SpecObjAll based on redshift values
            #Original spectra is emit
            #observed is what happens after spectra has been affected by redshift
            #redshift correction is retrieving original spectra
            #wikipedia says equation is (1+z = obs. wavelength / emitted wavelength)
            #Rearranged equation to get emitted wavelength
            for band in bands:
                if band not in self.data.columns:
                    continue  # Skip bands not present in the data
                corrected_values = self.data[band] / (1 + self.data['z'])
                self.data[band] = corrected_values
        else:
            raise ValueError("No wavelength data available for redshift correction")