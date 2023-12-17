"""This test module runs tests for cross_matching_module.py"""
import requests
import unittest
from unittest.mock import patch, MagicMock
from group9_package.subpkg_2.cross_matching_module import CrossMatchingModule


class TestCrossMatchingModule(unittest.TestCase):

    def setUp(self):
        """
        This function instantiates a reusable cross match instance.
        """

        self.cross_match_module = CrossMatchingModule()

    def test_successful_query(self):
        """
        This test verifies a successful query using an example source id found in the database.
        """

        result = self.cross_match_module.cross_match(1, '6279435494640163584')
        self.assertIsNotNone(result)
        self.assertFalse(result.empty)

    def test_angular_threshold(self):
        """
        This test verifies that no result is reported for matches above threshold.
        """

        result = self.cross_match_module.cross_match(0, 6279435494640163584)
        self.assertIsNotNone(result)
        self.assertTrue(result.empty)

    def test_invalid_angular_distance(self):
        """
        This test verifies that invalid typed angular distances are handled correctly.
        """
  
        with self.assertRaises(ValueError):
            self.cross_match_module.cross_match('lol', 6279435494640163584)

    def test_invalid_source_id(self):
        """
        This test verifies that invalid typed source id are handled correctly
        """
   
        with self.assertRaises(ValueError):
            self.cross_match_module.cross_match(1, 'lol')

    def test_neg_value_for_angular_distance(self):
        """
        This test verifies that a negative value for angular distance raises a value error
        """
 
        with self.assertRaises(ValueError):
            self.cross_match_module.cross_match(-1, 6279435494640163584)    

    def test_none_input(self):
        """
        This test verifies None inputs are handled properly
        """

        with self.assertRaises(TypeError):
            self.cross_match_module.cross_match(None, None)
    
    # Ensure server errors are handled
    @patch('astroquery.gaia.Gaia.launch_job')
    def test_internal_server_error(self, mock_launch_job):
        """
        This test verifies that server errors from gaia properly raise http error
        """
        # Create a mock job object with a mock get_results method
        mock_job = MagicMock()
        mock_job.get_results.side_effect = requests.exceptions.HTTPError("Simulated Gaia server error")
        mock_launch_job.return_value = mock_job

        cross_match_module = CrossMatchingModule()

        # Test handling of HTTPError
        with self.assertRaises(requests.exceptions.HTTPError):
            cross_match_module.cross_match(10, 6279435494640163584)

if __name__ == '__main__':
    unittest.main()
