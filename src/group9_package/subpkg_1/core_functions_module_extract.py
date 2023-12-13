#!/usr/bin/env python3
# File       : core_functions_module.py
# Description: Core functions module for spectral data analysis
# License    : GNU General Public License, version 3
# Copyright 2023 Harvard University. All Rights Reserved.

from astroquery.sdss import SDSS
from astropy.table import Table
from astroquery.exceptions import RemoteServiceError, TimeoutError
from requests.exceptions import RequestException
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
