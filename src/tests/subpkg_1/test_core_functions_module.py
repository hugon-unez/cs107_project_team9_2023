"""This test module runs tests for core_functions_module.py"""

from astroquery.sdss import sdss
from astropy.table import Table
from astroquery.exceptions import RemoteServiceError, TimeoutError
from requests.exceptions import RequestException

import pytest


class TestSpectralAnalysisBase():
    """A class for testing our methods in the base class"""

    def test_init(self):
        """This is a trivial test to ensure that tests the __init__ function"""

        # Initializing AstroQuery Class
        selected_object = 'pluto'
        astro = AstroQuery(selected_object)

        assert hasattr(astro, "temp1")
        assert hasattr(astro, "temp2")
        assert hasattr(astro, "selected_object")

    def test_execute_query(self):
        """This a trivial test to check the return value of extract"""

        # Calling extract 
        selected_object = 'pluto'
        astro = AstroQuery(selected_object)
        extract_information = astro.extract()
        
        # Manually performing query
        Gaia.MAIN_GAIA_TABLE = 'gaiadr3.gaia_source'

        query = f'''SELECT inclination, eccentricity, semi_major_axis FROM gaiadr3.sso_orbits WHERE denomination = '{selected_object}'
            '''
        job = Gaia.launch_job(query)
        data = job.get_results()
        a_df = data.to_pandas()
        temp1 = a_df
    
        query = f'''SELECT epoch, ra, dec, g_mag FROM gaiadr3.sso_observation WHERE astrometric_outcome_transit = 1 AND denomination = '{selected_object}'
            '''
        job = Gaia.launch_job(query)
        data = job.get_results()
        c_df = data.to_pandas()
        temp2 = c_df

        manual_information = (f'The denomination specified for both queries is {selected_object}. The table for observations is {temp1} and the table for orbits is {temp2}')
        
        assert manual_information == extract_information