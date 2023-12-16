#!/usr/bin/env python3
# File       : core_functions_module_extract.py
# Description: Extracts Astronomical Data from SDSS
# License    : GNU General Public License, version 3
# Copyright 2023 Harvard University. All Rights Reserved.
"""This python module provides functionality for querying and extracting astronomical data from the SDSS database. """

from astroquery.sdss import SDSS
from astropy.table import Table
from astroquery.exceptions import RemoteServiceError, TimeoutError
from requests.exceptions import RequestException
import pandas as pd
import requests
import io
import time

class SpectralAnalysisBase:
    """Foundational class for performing spectral analysis by querying and handling data from the SDSS database."""
    def __init__(self, query, data=None):
        """Initializes SpectralAnalysisBase Class

        Args:
            query (str): String parameter containing an ADQL query to query the SDSS database.
            data (astropy.table.Table, optional): Optional parameter to input spectral data as an Astropy Table object.
                Defaults to None.

        Raises:
            ValueError: If the given data is not an astropy table
        """
        self.query = query

        # Check that data is Table type, the type returned by query
        if data is not None and not isinstance(data, Table):
            raise ValueError("data must be an Astropy Table object")
        
        self.data = data

    @staticmethod
    def query_validation(query:str):
        """Validates the given query string to ensure it contains basic elements of a SQL query.

        Args:
            query (str): The query string to validate.

        Raises:
            ValueError: If the query string does not contain necessary SQL elements.
        """
        if 'select' not in query.lower() or 'from' not in query.lower():
            raise ValueError("Query is invalid.")

    def execute_query(self):
        """Executes the SQL query against the SDSS database and stores the result in the data attribute.

        Raises:
            RemoteServiceError, TimeoutError, ValueError, RequestException: For various errors that may occur during query execution.
        """
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
    """A Class for extracting user requested metadata"""
    def __init__(self, query, data=None):
        """Initializes MetadataExtractor Class

        Args:
            query (str): String parameter containing an ADQL query to query the SDSS database
            data (astropy.table.Table, optional): Optional parameter to input spectral data 
                as Astropy Table object. Default = None.
        """
        super().__init__(query, data)

    def extract_identifiers(self):
        """Extracts unique identifiers from the data.

        Returns:
            Astropy Table Column: A column of identifiers from the data.

        Raises:
            ValueError: If no data is available to extract identifiers or the 'bestObjID' column is missing.
        """        
        if self.data is None or 'bestObjID' not in self.data.colnames:
            raise ValueError("No data available to extract identifiers.")
        
        identifiers = self.data['bestObjID']
        return identifiers

    def extract_coordinates(self):
        """Extracts astronomical coordinates from the data.

        Returns:
            Astropy Table: A table containing the 'bestObjID', 'ra', and 'dec' columns.

        Raises:
            ValueError: If no data is available to extract coordinates or the required columns are missing.
        """
        coordinatesCol = ['bestObjID', 'ra', 'dec']
        if self.data is None or not all(item in self.data.colnames  for item in coordinatesCol):
            raise ValueError("No data available to extract coordinates.")
        
        coordinates = self.data['bestObjID', 'ra', 'dec']
        return coordinates

    def extract_chemical_abundances(self):
        """Extracts chemical abundances from the data.

        Returns:
            Astropy Table: A table containing the 'bestObjID' and 'elodieFeH' columns.

        Raises:
            ValueError: If no data is available to extract chemical abundances or the required columns are missing.
        """        
        chemicalAbundancesCol = ['bestObjID', 'elodieFeH']
        if self.data is None or not all(item in self.data.colnames  for item in chemicalAbundancesCol):
            raise ValueError("No data available to extract chemical abundances.")
        
        # find the actual column name in dataset
        chemical_abundances = self.data['bestObjID','elodieFeH']
        return chemical_abundances

    def extract_redshifts(self):
        """Extracts redshift values from the data.

        Returns:
            Astropy Table: A table containing the 'bestObjID' and 'elodieZ' columns.

        Raises:
            ValueError: If no data is available to extract redshifts or the required columns are missing.
        """        
        redshiftsCol = ['bestObjID','elodieZ'] 
        if self.data is None or not all(item in self.data.colnames for item in redshiftsCol):
            raise ValueError("No data available to extract redshifts.")
        
        redshifts = self.data['bestObjID','elodieZ']
        return redshifts

class SpectraExtract(SpectralAnalysisBase):
    """A Class for extracting spectral data for individual astronomical objects"""
    def __init__(self, data_row):
        """Initializes the SpectraExtract Class

        Args:
            data_row (Table.Row): A single row from an Astropy Table representing an astronomical object.

        Raises:
            TypeError: If the input is not an astropy.table.Row.
            ValueError: If the input row is missing required columns.
        """
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
        """Retrieves spectral data for the astronomical object represented by inputted data row.

        Returns:
            DataFrame: A Pandas DataFrame containing the spectral data.
        """
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