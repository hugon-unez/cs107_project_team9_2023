"""This unit test module runs tests for core_functions_module_extract.py"""

import unittest
import numpy as np
from unittest.mock import patch
from astropy.table import Table
from group9_package.subpkg_1.core_functions_module_extract import SpectralAnalysisBase, MetaDataExtractor, SpectraExtract
from astroquery.exceptions import RemoteServiceError, TimeoutError
from requests.exceptions import RequestException

class TestSpectralAnalysisBase(unittest.TestCase):
    """A class for testing our methods in the SpectralAnalysisBase Class"""
    def setUp(self):
        """
        Creating valid and invalid queries that we will use throughout the
        testing suite
        """
        self.valid_query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
        self.invalid_query = "Invalid Query"

    def test_init_with_valid_data(self):
        """Tests that the initialization attribute declarations work"""
        data = Table()
        base = SpectralAnalysisBase(self.valid_query, data=data)
        self.assertEqual(base.query, self.valid_query)
        self.assertIsInstance(base.data, Table)

    def test_init_with_invalid_data(self):
        """Tests that we raise ValueError when invalid data is inputted"""
        with self.assertRaises(ValueError):
            SpectralAnalysisBase(self.valid_query, data="invalid_data")

    def test_query_validation_valid_query(self):
        """Tests that no exception is raised with valid query"""
        SpectralAnalysisBase.query_validation(self.valid_query)

    def test_query_validation_invalid_query(self):
        """Tests that an invalid query raises ValueError"""
        with self.assertRaises(ValueError):
            SpectralAnalysisBase.query_validation(self.invalid_query)

    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_execute_query_success(self, mock_query_sql):
        """Test the execute query works with the mock so no dependcies on astropy"""
        result_data = Table()
        mock_query_sql.return_value = result_data
        base = SpectralAnalysisBase(self.valid_query)
        base.execute_query()
        self.assertIsInstance(base.data, Table)
    
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql', side_effect=RemoteServiceError("Service error"))
    def test_execute_query_remote_service_error(self, mock_query_sql):
        """
        Test that if execution of query gives RemoteServiceError that
        our method throws it as well
        """
        base = SpectralAnalysisBase(self.valid_query)
        with self.assertRaises(RemoteServiceError):
            base.execute_query()
    
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql', side_effect=TimeoutError("Timeout error"))
    def test_execute_query_timeout_error(self, mock_query_sql):
        """
        Tests that if execution of query gives us TimeoutError that
        our method throws it as well
        """
        base = SpectralAnalysisBase(self.valid_query)
        with self.assertRaises(TimeoutError):
            base.execute_query()

    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql', side_effect=RequestException("Request exception"))
    def test_execute_query_request_exception(self, mock_query_sql):
        """
        Tests that if execution of query gives us RequestException that
        our method throws it as well
        """
        base = SpectralAnalysisBase(self.valid_query)
        with self.assertRaises(RequestException):
            base.execute_query()

class TestMetaDataExtractor(unittest.TestCase):
    """A class for testing our methods in the MetaDataExtractor Class"""

    def setUp(self):
        """
        Creating valid and invalid queries that we will use throughout the
        testing suite
        """
        self.valid_query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
        self.invalid_query = "Invalid Query"

    def test_extract_identifiers_with_valid_data(self):
        """Tests extract identifiers method with valid data and it has correct output"""
        data = Table({'bestObjID': [1, 2, 3]})
        extractor = MetaDataExtractor(self.valid_query, data)
        identifiers = extractor.extract_identifiers()
        self.assertEqual(identifiers.tolist(), [1, 2, 3])

    def test_extract_identifiers_with_invalid_data(self):
        """
        Tests extract identifiers method with invalid data and 
        that an error is thrown
        """
        extractor = MetaDataExtractor(self.invalid_query)
        with self.assertRaises(ValueError):
            extractor.extract_identifiers()

    def test_extract_coordinates_with_valid_data(self):
        """Tests extract coordinates method with valid data and it has correct output"""
        data = Table({'bestObjID': [1, 2, 3],'ra':[1,2,3], 'dec':[1,2,3]})
        extractor = MetaDataExtractor(self.valid_query, data)
        coordinates = extractor.extract_coordinates()
        self.assertEqual(coordinates.to_pandas().values.tolist(), [[1, 1, 1], [2, 2, 2], [3, 3, 3]])

    def test_extract_coordinates_with_invalid_data(self):
        """
        Tests extract coordinates method with invalid data and 
        that an error is thrown
        """
        extractor = MetaDataExtractor(self.invalid_query)
        with self.assertRaises(ValueError):
            extractor.extract_coordinates()

    def test_extract_chemical_abundances_with_valid_data(self):
        """Tests extract chemical abundances method with valid data and it has correct output"""
        data = Table({'bestObjID': [1, 2, 3],'elodieFeH':[1,2,3]})
        extractor = MetaDataExtractor(self.valid_query, data)
        chemical_abundances = extractor.extract_chemical_abundances()
        self.assertEqual(chemical_abundances.to_pandas().values.tolist(), [[1, 1], [2, 2], [3, 3]])
    
    def test_extract_chemical_abundances_with_invalid_data(self):
        """
        Tests extract chemical abundances method with invalid data and 
        that it throws error
        """
        extractor = MetaDataExtractor(self.invalid_query)
        with self.assertRaises(ValueError):
            extractor.extract_chemical_abundances()

    def test_extract_redshifts_with_valid_data(self):
        """Tests extract redshifts method with valid data and it has correct output"""
        data = Table({'bestObjID': [1, 2, 3],'elodieZ':[1,2,3]})
        extractor = MetaDataExtractor(self.valid_query, data)
        redshifts = extractor.extract_redshifts()
        self.assertEqual(redshifts.to_pandas().values.tolist(), [[1, 1], [2, 2], [3, 3]])

    def test_extract_redshifts_with_invalid_data(self):
        """
        Tests extract redshifts method with invalid data and 
        that it throws error
        """
        extractor = MetaDataExtractor(self.invalid_query)
        with self.assertRaises(ValueError):
            extractor.extract_redshifts()

class TestSpectraExtract(unittest.TestCase):
    """A class for testing our methods in the SpectraExtract Class"""
    def test_spectra_extract(self):
        """Tests extract spectra method

        Specifically, ensures that our instance variables are 
        assigned correctly if our query to SDSS returns spectral data
        """
        # Create an instance of spectraExtract with sample data from sdss docs

        # sample_row = Row({'plate': 15150, 'mjd': 59291, 'fiberid': 1})
        row_data = {'plate': np.array([15150]), 'mjd': np.array([59291]), 'fiberid': np.array([1])}
        table = Table(row_data, names=('plate', 'mjd', 'fiberid'))

        extractor = SpectraExtract(table[0])

        data = extractor.extract_spectra()

        # make sure dataframe not empty
        self.assertFalse(data.empty, "DataFrame should not be empty")

        # make sure dataframe has correct columns
        self.assertCountEqual(['Wavelength', 'Flux', 'BestFit', 'SkyFlux'], data.columns.tolist())

        data_full = extractor.extract_spectra_full()

        # make sure dataframe not empty
        self.assertFalse(data_full.empty, "DataFrame should not be empty")

        # make sure dataframe has correct columns
        self.assertCountEqual(['FLUX', 'LOGLAM', 'IVAR', 'AND_MASK', 'OR_MASK', 'WDISP', 'SKY', 'WRESL', 'MODEL'], data_full.columns.tolist())

if __name__ == '__main__':
    unittest.main()