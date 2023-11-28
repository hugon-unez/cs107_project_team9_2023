"""This test module runs tests for core_functions_module.py"""

from astroquery.sdss import SDSS
from astropy.table import Table
from astroquery.exceptions import RemoteServiceError, TimeoutError
from requests.exceptions import RequestException
from src.group9_package.subpkg_1.core_functions_module import SpectralAnalysisBase
import pytest


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
        query = f'''SELECT epoch, ra, dec, g_mag FROM gaiadr3.sso_observation WHERE astrometric_outcome_transit = 1 AND denomination = 'pluto'
            '''
        astro = SpectralAnalysisBase(query)
        astro.execute_query()
        
        # Manually performing query
        data = Table(SDSS.query_sql(query))

        assert data == astro.data

        # Test invalid query Value Error Raised no Select

        query = f'''invalid query test
            '''
        astro = SpectralAnalysisBase(query)

        with pytest.raises(ValueError):
            astro.execute_query()

        # Test invalid query Value Error Raised no Select

        query = f'''select query test
            '''
        astro = SpectralAnalysisBase(query)

        with pytest.raises(ValueError):
            astro.execute_query()

        # Test setting data not equal to Table Astroquery DataType

        query = f'''SELECT epoch, ra, dec, g_mag FROM gaiadr3.sso_observation WHERE astrometric_outcome_transit = 1 AND denomination = 'pluto'
            '''

        with pytest.raises(ValueError):
            astro = SpectralAnalysisBase(query,data=[])