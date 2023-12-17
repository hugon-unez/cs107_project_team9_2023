"""
This integration test module runs tests for core_functions_module_modify.py.
Specifically, it ensures that all of our classes within the module work dependently
"""
import unittest
import numpy as np
import pandas as pd
from group9_package.subpkg_1.core_functions_module_modify import DataPreprocessor

class TestDataPreprocessor(unittest.TestCase):
    """A class for testing our methods in the DataPreprocessor Class"""
    
    def setUp(self):
        """Tests Setup Testing Environment for Integration
        
        Data is passed in to ensure results integrate well together
        """
        self.query = "select top 10 ra, dec, bestObjID from specObj where class = 'galaxy' and z > 0.3 and zWarning = 0"
        self.test_data = pd.DataFrame({
            'wavelength': np.arange(10),
            'flux': np.random.rand(10),
            'z': np.random.rand(10)
        })
    
    def test_data_preprocessing_pipeline(self):
        """Tests All Data Preprocessing Methods work together
        
        Confirm Equivalence and values for each method and column
        """
        data_preprocessor = DataPreprocessor(query=self.query, data=self.test_data.copy())

        data_preprocessor.normalize_data()
        data_preprocessor.remove_outliers()

        data_preprocessor.interpolate_data([2,4,6,8,10,12,14,16,18,20])

        data_preprocessor.correct_redshift()

        #assert every column 'flux' row is populated
        self.assertTrue(all(np.isfinite(data_preprocessor.data['flux'])))

        #assert every column 'wavelength' row is populated
        self.assertTrue(all(np.isfinite(data_preprocessor.data['wavelength'])))

        #assert every column 'z' row is populated
        self.assertTrue(all(np.isfinite(data_preprocessor.data['z'])))

        #assert first row value is equivalent to what we expect
        self.assertAlmostEqual(data_preprocessor.data['wavelength'][0], -1.5666699, places=4)

if __name__ == '__main__':
    unittest.main()