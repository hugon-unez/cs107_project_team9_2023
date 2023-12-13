import unittest
from unittest.mock import patch
from astropy.table import Table
import pandas as pd
import numpy as np
from group9_package.subpkg_1.core_functions_module_extract import SpectralAnalysisBase, MetaDataExtractor, DataPreprocessor
from astroquery.exceptions import RemoteServiceError, TimeoutError
from requests.exceptions import RequestException

class TestSpectralAnalysisBase(unittest.TestCase):
    def setUp(self):
        self.valid_query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
        self.invalid_query = "Invalid Query"

    #test the initialization attribute declarations work
    def test_init_with_valid_data(self):
        data = Table()
        base = SpectralAnalysisBase(self.valid_query, data=data)
        self.assertEqual(base.query, self.valid_query)
        self.assertIsInstance(base.data, Table)

    def test_init_with_invalid_data(self):
        with self.assertRaises(ValueError):
            SpectralAnalysisBase(self.valid_query, data="invalid_data")

    def test_query_validation_valid_query(self):
        # No exception should be raised with query
        SpectralAnalysisBase.query_validation(self.valid_query)

    def test_query_validation_invalid_query(self):
        # Invalid query should raise ValueErrors
        with self.assertRaises(ValueError):
            SpectralAnalysisBase.query_validation(self.invalid_query)

    #test the execute query works with the mock so no dependcies on astropy
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_execute_query_success(self, mock_query_sql):
        result_data = Table()
        mock_query_sql.return_value = result_data
        base = SpectralAnalysisBase(self.valid_query)
        base.execute_query()
        self.assertIsInstance(base.data, Table)
    
    #test remote error throws appropriate error
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql', side_effect=RemoteServiceError("Service error"))
    def test_execute_query_remote_service_error(self, mock_query_sql):
        base = SpectralAnalysisBase(self.valid_query)
        with self.assertRaises(RemoteServiceError):
            base.execute_query()
    
    #test execute query throws appropriate error
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql', side_effect=TimeoutError("Timeout error"))
    def test_execute_query_timeout_error(self, mock_query_sql):
        base = SpectralAnalysisBase(self.valid_query)
        with self.assertRaises(TimeoutError):
            base.execute_query()

    #test request exception throws appropriate error
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql', side_effect=RequestException("Request exception"))
    def test_execute_query_request_exception(self, mock_query_sql):
        base = SpectralAnalysisBase(self.valid_query)
        with self.assertRaises(RequestException):
            base.execute_query()

class TestMetaDataExtractor(unittest.TestCase):
    #initialize class
    def setUp(self):
        self.valid_query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy'  and z > 0.3 and zWarning = 0"
        self.invalid_query = "Invalid Query"

    #test extract identifiers with valid data
    def test_extract_identifiers_with_valid_data(self):
        data = Table({'bestObjID': [1, 2, 3]})
        extractor = MetaDataExtractor(self.valid_query, data)
        identifiers = extractor.extract_identifiers()
        self.assertEqual(identifiers.tolist(), [1, 2, 3])

    #test extract identifiers with invalid data and assert error thrown
    def test_extract_identifiers_with_invalid_data(self):
        extractor = MetaDataExtractor(self.invalid_query)
        with self.assertRaises(ValueError):
            extractor.extract_identifiers()

    #test extract coordinates with valid data has correct form
    def test_extract_coordinates_with_valid_data(self):
        data = Table({'bestObjID': [1, 2, 3],'ra':[1,2,3], 'dec':[1,2,3]})
        extractor = MetaDataExtractor(self.valid_query, data)
        coordinates = extractor.extract_coordinates()
        self.assertEqual(coordinates.to_pandas().values.tolist(), [[1, 1, 1], [2, 2, 2], [3, 3, 3]])

    #test extract coordinates with invalid data and assert error thrown
    def test_extract_coordinates_with_invalid_data(self):
        extractor = MetaDataExtractor(self.invalid_query)
        with self.assertRaises(ValueError):
            extractor.extract_coordinates()

    #test extract chemical abundances with valid data has correct form
    def test_extract_chemical_abundances_with_valid_data(self):
        data = Table({'bestObjID': [1, 2, 3],'elodieFeH':[1,2,3]})
        extractor = MetaDataExtractor(self.valid_query, data)
        chemical_abundances = extractor.extract_chemical_abundances()
        self.assertEqual(chemical_abundances.to_pandas().values.tolist(), [[1, 1], [2, 2], [3, 3]])
    
    #test extract chemical abundances with invalid data throws error
    def test_extract_coordinates_with_invalid_data(self):
        extractor = MetaDataExtractor(self.invalid_query)
        with self.assertRaises(ValueError):
            extractor.extract_chemical_abundances()

    #test extract redshifts with valid data has correct form
    def test_extract_redshifts_with_valid_data(self):
        data = Table({'bestObjID': [1, 2, 3],'elodieZ':[1,2,3]})
        extractor = MetaDataExtractor(self.valid_query, data)
        redshifts = extractor.extract_redshifts()
        self.assertEqual(redshifts.to_pandas().values.tolist(), [[1, 1], [2, 2], [3, 3]])

    #test extract redshifts with invalid data throws error
    def test_extract_redshifts_with_invalid_data(self):
        extractor = MetaDataExtractor(self.invalid_query)
        with self.assertRaises(ValueError):
            extractor.extract_redshifts()

class TestDataPreprocessor(unittest.TestCase):
    def setUp(self):
        self.valid_query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy' and z > 0.3 and zWarning = 0"
        self.invalid_query = "Invalid Query"

    # Test initialization with valid data
    @patch('group9_package.subpkg_1.core_functions_module_extract.SDSS.query_sql')
    def test_init_with_valid_data(self, mock_query_sql):
        result_data = pd.DataFrame({'ra': [1, 2, 3], 'dec': [4, 5, 6], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        mock_query_sql.return_value = result_data

        data = pd.DataFrame()  # Use pandas DataFrame here
        base = SpectralAnalysisBase(self.valid_query, data=data)
        self.assertEqual(base.query, self.valid_query)
        self.assertIsInstance(base.data, pd.DataFrame)

    # Test initialization with invalid data
    def test_init_with_invalid_data(self):
        with self.assertRaises(ValueError):
            DataPreprocessor(self.valid_query, data="invalid_data")

    # Test normalization
    def test_normalize_data(self):
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        data_preprocessor = DataPreprocessor(self.valid_query, data=data)
        data_preprocessor.normalize_data()

        for header in data_preprocessor.column_headers:
            normalized_data = (data[header] - np.mean(data[header])) / np.std(data[header])
            np.testing.assert_array_almost_equal(data_preprocessor.data[header], normalized_data)

    # Test outlier removal
    def test_remove_outliers(self):
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        data_preprocessor = DataPreprocessor(self.valid_query, data=data)
        data_preprocessor.remove_outliers()

        for header in data_preprocessor.column_headers:
            z_scores = np.abs((data[header] - np.mean(data[header])) / np.std(data[header]))
            outliers_removed = data[header][z_scores < 2.5]
            np.testing.assert_array_almost_equal(data_preprocessor.data[header], outliers_removed)

    # Test interpolation
    def test_interpolate_data(self):
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        data_preprocessor = DataPreprocessor(self.valid_query, data=data)

        new_wavelengths = np.array([1.1, 1.2, 1.3, 1.4])
        data_preprocessor.interpolate_data(new_wavelengths)

        for header in data_preprocessor.column_headers:
            interp_function = np.interp(new_wavelengths, data.index, data[header])
            np.testing.assert_array_almost_equal(data_preprocessor.data[header], interp_function)

    # Test redshift correction
    def test_correct_redshift(self):
        data = pd.DataFrame({'ra': [1, 2, 3], 'u': [7, 8, 9], 'g': [10, 11, 12], 'r': [13, 14, 15], 'i': [16, 17, 18], 'z': [0.4, 0.5, 0.6]})
        data_preprocessor = DataPreprocessor(self.valid_query, data=data)

        bands = ['u', 'g', 'r', 'i']
        data_preprocessor.correct_redshift(bands)

        for band in bands:
            corrected_values = data[band] / (1 + data['z'])
            np.testing.assert_array_almost_equal(data_preprocessor.data[band], corrected_values)

if __name__ == '__main__':
    unittest.main()
