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
        self.query = query

        # Check that data is Table type, the type returned by query
        if data is not None and not isinstance(data, Table):
            raise ValueError("data must be an Astropy Table object")
        
        self.data = data

    def execute_query(self):
        # use try except block in order to catch issues with query
        try:
            result = SDSS.query_sql(self.query)
            self.data = Table(result)
        except (RemoteServiceError, TimeoutError) as e:
            print(f"Query Error: {e}")
        except RequestException as e:
            print(f"RequestException: {e}")
        else:
            print("Query executed successfully and result stored in data attribute.")


def main():
    query = "select top 10 XYA, ra, dec, bestObjID from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
    res = SDSS.query_sql(query)
    print(res[:5])

if __name__ == "__main__":
    main()