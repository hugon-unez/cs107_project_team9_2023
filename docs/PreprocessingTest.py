import unittest
from unittest.mock import patch
from core_functions_module_extract import SpectralAnalysisBase
import numpy as np
import pandas as pd
from astropy.table import Table
from astroquery.exceptions import RemoteServiceError, TimeoutError
from requests.exceptions import RequestException
from Preprocessing import DataPreprocessor

class TestDataPreprocessor(unittest.TestCase):
    def setUp(self):
        self.valid_query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy' and z > 0.3 and zWarning = 0"
        self.invalid_query = "Invalid Query"

    # Test initialization with valid data
    @patch('core_functions_module_extract.SDSS.query_sql')
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