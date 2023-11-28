"""This test module runs tests for core_functions_module.py"""

import pytest
from astroquery.sdss import SDSS
from astropy.table import Table
from astropy.utils.diff import report_diff_values
from astroquery.exceptions import RemoteServiceError, TimeoutError
from requests.exceptions import RequestException
from group9_package.subpkg_1.core_functions_module import SpectralAnalysisBase

class TestSpectralAnalysisBase():
    """A class for testing our methods in the base class"""

    def test_init(self):
        """This is a trivial test to ensure that tests the __init__ function"""

        # Initializing Core Class
        query = f'''SELECT epoch, ra, dec, g_mag FROM gaiadr3.sso_observation WHERE astrometric_outcome_transit = 1 AND denomination = 'pluto'
            '''
        astro = SpectralAnalysisBase(query)

        assert hasattr(astro, "query")
        assert hasattr(astro, "data")

    def test_execute_query(self):
        """This a trivial test to check the return value of extract"""

        # Calling execute query 
        
        query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
        astro = SpectralAnalysisBase(query)
        astro.execute_query()

        # Manually performing query
        result = SDSS.query_sql(query)
        data = Table(result)

        assert report_diff_values(data, astro.data)

        # Test invalid query Value Error Raised no Select

        query = 'invalid query test'
        astro1 = SpectralAnalysisBase(query)

        with pytest.raises(ValueError):
            astro1.execute_query()

        # # Test invalid query Value Error Raised no Select

        query = "select query test"
        astro = SpectralAnalysisBase(query)

        with pytest.raises(ValueError):
            astro.execute_query()

        # # Test setting data not equal to Table Astroquery DataType

        query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"

        with pytest.raises(ValueError):
            astro = SpectralAnalysisBase(query,data=[])