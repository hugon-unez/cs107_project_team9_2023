"""
This integration test module runs tests for core_functions_module_extract.py.
Specifically, it ensures that all of our classes within the module work dependently
"""

import pytest
import unittest
import numpy as np
from astroquery.sdss import SDSS
from astropy.table import Table, Column, Row
from astropy.utils.diff import report_diff_values
from group9_package.subpkg_1.core_functions_module_extract import SpectralAnalysisBase, MetaDataExtractor, SpectraExtract

class TestSpectralAnalysisBase():
    """A class for testing our methods in the SpectralAnalysisBase Class"""
    def test_init(self):
        """This is a trivial test to ensure our class has the appropriate instance variables"""
        # Initializing Core Class
        query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
        astro = SpectralAnalysisBase(query)

        assert hasattr(astro, "query")
        assert hasattr(astro, "data")

    def test_execute_query(self):
        """Tests execute query method

        Specifically, ensures that we raise ValueError on invalid
        queries and if the data inputted is not of type Astropy Table
        """
        # Calling execute query 
        query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
        astro = SpectralAnalysisBase(query)
        astro.execute_query()

        # Manually performing query
        result = SDSS.query_sql(query)
        data = Table(result)

        assert report_diff_values(data, astro.data)

        # Test invalid query Value Error Raised no 'Select'

        query = 'invalid query test'
        astro1 = SpectralAnalysisBase(query)

        with pytest.raises(ValueError):
            astro1.execute_query()

        # Test invalid query Value Error Raised no 'From'

        query = "select query test"
        astro = SpectralAnalysisBase(query)

        with pytest.raises(ValueError):
            astro.execute_query()

        # Test setting data not equal to Table Astroquery DataType

        query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"

        with pytest.raises(ValueError):
            astro = SpectralAnalysisBase(query,data=[])

class TestSpectralAnalysisMetaDataExtractor():
    """A class for testing our methods in the MetaDataExtractor Class"""
    def test_init(self):
        """This is a trivial test to ensure our class has the appropriate instance variables"""
        # Initializing Core Class
        query = "select top 10 ra, dec, z, bestObjID from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
        astro = MetaDataExtractor(query)

        assert hasattr(astro, "query")
        assert hasattr(astro, "data")


    def test_extract_methods(self):
        """Tests all extract methods 

        Specifically, ensures that we raise a ValueError when the methods are
        called and the query was never executed, that the returned objects of our 
        methods have the correct types, that our returned objects contain the 
        correct columns, and that we raise a ValueError when we try extracting 
        metadata when it is not present in our DataFrame of data
        """
        query = "select top 10 ra, dec, elodieZ, bestObjID, elodieFeH from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
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
        chemicalAbundances = astro.extract_chemical_abundances()
        redshifts = astro.extract_redshifts()

        #assert return types are correct and standardized 
        assert type(identifiers) == Column
        assert type(coordinates) == Table
        assert type(chemicalAbundances) == Table
        assert type(redshifts) == Table

        #assert each Table has at least necessary column headers
        identifiersCol = ['bestObjID']
        coordinatesCol = ['bestObjID', 'ra', 'dec']
        chemicalAbundancesCol = ['bestObjID', 'elodieFeH']
        redshiftsCol = ['bestObjID','elodieZ']

        assert identifiers.name in identifiersCol
        assert all(item in coordinates.colnames for item in coordinatesCol)
        assert all(item in chemicalAbundances.colnames for item in chemicalAbundancesCol)
        assert all(item in redshifts.colnames for item in redshiftsCol)

        #query does not request bestObjID
        bad_query = "select top 10 ra, dec, z from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
        astro1 = MetaDataExtractor(bad_query)

        #test value errors are raised if required column is not present
        with pytest.raises(ValueError):
            astro1.extract_identifiers()

### NEED TO ADD INTEGRATION TEST FOR SPECTRA EXTRACT