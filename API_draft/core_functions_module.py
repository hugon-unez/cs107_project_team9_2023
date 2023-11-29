#!/usr/bin/env python3
# File       : core_functions_module.py
# Description: Core functions module for spectral data analysis
# License    : GNU General Public License, version 3
# Copyright 2023 Harvard University. All Rights Reserved.

from astroquery.sdss import SDSS
from astropy.table import Table
from astroquery.exceptions import RemoteServiceError, TimeoutError
from requests.exceptions import RequestException

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
        except RequestException as e:
            print(f"RequestException: {e}")
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
        if self.data is None:
            raise ValueError("No data available to extract identifiers.")
        
        identifiers = self.data['bestObjID']
        return identifiers

    def extract_coordinates(self):
        # extracts coordinates from the data
        if self.data is None:
            raise ValueError("No data available to extract coordinates.")
        
        coordinates = self.data['ra', 'dec']
        return coordinates

    # below needs to be adjusted for correct chemical abundance colums
    def extract_chemical_abundances(self):
        # extracts chemical abundances 
        # assume the chemical abundances are stored in specific columns in the data
        if self.data is None:
            raise ValueError("No data available to extract chemical abundances.")
        
        # find the actual column name in dataset
        chemical_abundances = self.data['chemical_abundance_column']
        return chemical_abundances

    def extract_redshifts(self):
        # extracts redshift values 
        if self.data is None:
            raise ValueError("No data available to extract redshifts.")
        
        redshifts = self.data['z']
        return redshifts


def main():
    query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
    analysis_instance = SpectralAnalysisBase(query)
    analysis_instance.execute_query()

if __name__ == "__main__":
    main()