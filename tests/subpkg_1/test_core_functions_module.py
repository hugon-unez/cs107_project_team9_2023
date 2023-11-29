"""This test module runs tests for core_functions_module.py"""

import pytest
from astroquery.sdss import SDSS
from astropy.table import Table, Column
from astropy.utils.diff import report_diff_values
from group9_package.subpkg_1.core_functions_module import SpectralAnalysisBase, MetaDataExtractor

class TestSpectralAnalysisBase():
    """A class for testing our methods in the base class"""

    def test_init(self):
        """This is a trivial test to ensure that tests the __init__ function"""

        # Initializing Core Class
        query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
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

class TestSpectralAnalysisMetaDataExtractor():
    """A class for testing our methods in the base class"""

    def test_init(self):
        """This is a trivial test to ensure that tests the __init__ function"""

        # Initializing Core Class
        query = "select top 10 ra, dec, z, bestObjID from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
        astro = MetaDataExtractor(query)

        assert hasattr(astro, "query")
        assert hasattr(astro, "data")


    def test_extract_methods(self):
        query = "select top 10 ra, dec, z, bestObjID from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
        astro = MetaDataExtractor(query)

        #test value errors are raised if query is never executed
        with pytest.raises(ValueError):
            astro.extract_identifiers()

        #test value errors are raised if query is never executed
        with pytest.raises(ValueError):
            astro.extract_coordinates()

        #test value errors are raised if query is never executed
        with pytest.raises(ValueError):
            astro.extract_chemical_abundances()

        #test value errors are raised if query is never executed
        with pytest.raises(ValueError):
            astro.extract_redshifts()

        astro.execute_query()

        identifiers = astro.extract_identifiers()
        coordinates = astro.extract_coordinates()
        #chemicalAbundances = astro.extract_chemical_abundances()
        redshifts = astro.extract_redshifts()

        #assert return types are correct and standardized 
        assert type(identifiers) == Column
        assert type(coordinates) == Table
        #assert type(chemicalAbundances) == Table
        assert type(redshifts) == Table

        #assert each Table has at least necessary column headers
        identifiersCol = ['bestObjID']
        coordinatesCol = ['bestObjID', 'ra', 'dec']
        #chemicalAbundancesCol = ['bestObjID', 'chemicalAbundance']
        redshiftsCol = ['bestObjID','z']

        assert identifiers.name in identifiersCol
        assert all(item in coordinates.colnames  for item in coordinatesCol)
        #assert chemicalAbundances.colnames in chemicalAbundancesCol
        assert all(item in redshifts.colnames  for item in redshiftsCol)

        #query does not request bestObjID
        bad_query = "select top 10 ra, dec, z from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
        astro1 = MetaDataExtractor(bad_query)

        #test value errors are raised if required column is not present
        with pytest.raises(ValueError):
            astro1.extract_identifiers()