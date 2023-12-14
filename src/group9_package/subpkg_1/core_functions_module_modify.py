#!/usr/bin/env python3
# File       : core_functions_module_modify.py
# Description: Core functions Modify Module for spectral data analysis
# License    : GNU General Public License, version 3
# Copyright 2023 Harvard University. All Rights Reserved.

from astroquery.sdss import SDSS
from scipy.interpolate import interp1d
from scipy.stats import zscore
import numpy as np
import pandas as pd
from group9_package.subpkg_1.core_functions_module_extract import SpectralAnalysisBase


class DataPreprocessor(SpectralAnalysisBase):
    #Spectral Data:
    #Definition: Spectral data represents how the intensity of light emitted or received 
    #by an object varies across different wavelengths. Representation: A spectrum is often 
    #presented as a graph where the x-axis represents the wavelength (or frequency) of light
    #and the y-axis represents the intensity or flux of light at each wavelength.

    #For light waves, the wavelength corresponds to the distance between two successive 
    #peaks or troughs of the electromagnetic wave.

    #User is expected to provide the query
    def __init__(self, query, data=None):

        #Similar to pp6 in that we're turning the query into a pandas dataframe
        self.query = query

        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame")

        job = SDSS.query_sql(self.query)
        self.data = job.to_pandas()

        self.column_headers = list(self.data.columns)

    def normalize_data(self):
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
        if self.data is not None:
            for header in self.column_headers:
                # Remove outliers from data in using z-score
                z_scores = np.abs(zscore(self.data[header]))
                outliers_removed = self.data[header][z_scores < threshold]
                self.data[header] = outliers_removed
        else:
            raise ValueError("No data available for outlier removal")

    #Interpolation is commonly employed when you have a set of discrete data points 
    #and you want to estimate the values at positions that are not explicitly provided.
    def interpolate_data(self, new_wavelengths):
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
            interp_function = interp1d(old_wavelengths, flux_values, kind='cubic', fill_value="extrapolate", bounds_error=False)

            # Use the interpolation function to estimate values at new_wavelengths
            interpolated_values = interp_function(new_wavelengths)

            # Update the dataframe with the interpolated values
            self.data[header_flux] = interpolated_values
        else:
            raise ValueError("No data available for interpolation")

    #the light emitted by distant objects undergoes a redshift, meaning that the wavelengths of the 
    #Emitted light are stretched and shifted towards the longer, "red" end of the electromagnetic spectrum.
    #the redshift of an object is directly proportional to its distance from an observer due to the expansion 
    # of the universe. The farther an object is, the greater its redshift tends to be.

    def correct_redshift(self, bands=['u', 'g', 'r', 'i']):
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