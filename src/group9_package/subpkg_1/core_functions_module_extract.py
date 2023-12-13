#!/usr/bin/env python3
# File       : core_functions_module.py
# Description: Core functions module for spectral data analysis
# License    : GNU General Public License, version 3
# Copyright 2023 Harvard University. All Rights Reserved.

from astroquery.sdss import SDSS
from astropy.table import Table
from astroquery.exceptions import RemoteServiceError, TimeoutError
from requests.exceptions import RequestException
from scipy.interpolate import interp1d
from scipy.stats import zscore
import numpy as np
import pandas as pd
import requests
import io
import time

class SpectralAnalysisBase:
    def __init__(self, query, data=None):
        """Initializes the base class for spectral analysis class

        Args:
            query (str): String parameter containing an ADQL query to query the SDSS database.
            data (astropy.table.Table, optional): Optional parameter to input spectral data as an Astropy Table object.
                Defaults to None.
        """
        self.query = query

        # Check that data is Table type, the type returned by query
        if data is not None and not isinstance(data, Table):
            raise ValueError("data must be an Astropy Table object")
        
        self.data = data

    # helper function to catch obviously invalid queries
    @staticmethod
    def query_validation(query:str):
        if 'select' not in query.lower() or 'from' not in query.lower():
            raise ValueError("Query is invalid.")

    def execute_query(self):
        # use try except block in order to catch issues with query
        try:
            self.query_validation(self.query)  # Validate the query before executing
            result = SDSS.query_sql(self.query)
            self.data = Table(result)
        except (RemoteServiceError, TimeoutError, ValueError) as e:
            print(f"Query Error: {e}")
            raise
        except RequestException as e:
            print(f"RequestException: {e}")
            raise
        else:
            print("Query executed successfully and result stored in data attribute.")
        
class MetaDataExtractor(SpectralAnalysisBase):
    def __init__(self, query, data=None):
        # Initializes MetadataExtractor class

        #    Args:
        #     query (str): String parameter containing an ADQL query to query the SDSS database
        #     data (astropy.table.Table, optional): Optional parameter to input spectral data as Astropy Table object
        #         Default = None.
        
        super().__init__(query, data)

    def extract_identifiers(self):
        # extracts identifiers from the data
        if self.data is None or 'bestObjID' not in self.data.colnames:
            raise ValueError("No data available to extract identifiers.")
        
        identifiers = self.data['bestObjID']
        return identifiers

    def extract_coordinates(self):
        # extracts coordinates from the data
        coordinatesCol = ['bestObjID', 'ra', 'dec']
        if self.data is None or not all(item in self.data.colnames  for item in coordinatesCol):
            raise ValueError("No data available to extract coordinates.")
        
        coordinates = self.data['bestObjID', 'ra', 'dec']
        return coordinates

    # below needs to be adjusted for correct chemical abundance colums
    def extract_chemical_abundances(self):
        # extracts chemical abundances 
        # assume the chemical abundances are stored in specific columns in the data
        chemicalAbundancesCol = ['bestObjID', 'elodieFeH']
        if self.data is None or not all(item in self.data.colnames  for item in chemicalAbundancesCol):
            raise ValueError("No data available to extract chemical abundances.")
        
        # find the actual column name in dataset
        chemical_abundances = self.data['bestObjID','elodieFeH']
        return chemical_abundances

    def extract_redshifts(self):
        # extracts redshift values
        redshiftsCol = ['bestObjID','elodieZ'] 
        if self.data is None or not all(item in self.data.colnames for item in redshiftsCol):
            raise ValueError("No data available to extract redshifts.")
        
        redshifts = self.data['bestObjID','elodieZ']
        return redshifts

class SpectraExtract(SpectralAnalysisBase):
    def __init__(self, data_row):
        if not isinstance(data_row, Table.Row):
            raise TypeError("The input must be an astropy.table.Row")
    
        # check we have the proper identifiers to query
        required_columns = ['plate', 'mjd', 'fiberid']
        missing_columns = [col for col in required_columns if col not in data_row.colnames]

        # raise value error if not
        if missing_columns:
            raise ValueError(f"The input row is missing required columns: {missing_columns}")
        
        # if data is proper, save row to self
        self.row = data_row
        
    def extract_spectra(self):
        # Initialize values to query
        row = self.row
        plate = row['plate']
        mjd = row['mjd']
        fiberid = row['fiberid']

        # Use initialized values for url
        url = f'http://dr18.sdss.org/optical/spectrum/view/data/format=csv/spec=lite?plateid={plate}&mjd={mjd}&fiberid={fiberid}'

        # Since site is faulty, retry a few times - error 500 is common even with a correct query
        retries = 5  
        delay = 2  

        for i in range(retries):
            response = requests.get(url)

            if response.status_code == 200:
                df = pd.read_csv(io.StringIO(response.text))
                print('Successful Query!')
                return df
            else:
                print(f'Request failed with status code: {response.status_code}. Retrying...')
                time.sleep(delay)  # Adding a delay before the next retry

        #print failure message
        print(f'Request failed after {retries} retries. Ensure proper row was input or try again later.')

class DataPreprocessor(SpectralAnalysisBase):
    #Spectral Data:
    #Definition: Spectral data represents how the intensity of light emitted or received 
    #by an object varies across different wavelengths. Representation: A spectrum is often 
    #presented as a graph where the x-axis represents the wavelength (or frequency) of light
    #and the y-axis represents the intensity or flux of light at each wavelength.

    #For light waves, the wavelength corresponds to the distance between two successive 
    #peaks or troughs of the electromagnetic wave.

    #User is expected to provide the query
    def __init__(self, query, data):

        #Similar to pp6 in that we're turning the query into a pandas dataframe
        self.query = query

        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame")


        self.data = data

        job = SDSS.query_sql(self.query)
        #r = job.get_results()
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
            if len(new_wavelengths) != len(self.data.index):
                raise ValueError("Length of new_wavelengths does not match length of index")
            
            for header in self.column_headers:
                #spectral data probably observes non-linear relationship
                interp_function = interp1d(self.data.index, self.data[header], kind='cubic', fill_value="extrapolate", bounds_error=False )

                # Use the interpolation function to estimate values at new_wavelengths
                interpolated_values = interp_function(new_wavelengths)

                # Update the dataframe with the interpolated values
                self.data[header] = interpolated_values
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