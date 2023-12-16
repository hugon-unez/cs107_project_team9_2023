import unittest
from group9_package.subpkg_2.cross_matching_module import CrossMatchingModule


class TestCrossMatchingModule(unittest.TestCase):

    def setUp(self):
        self.cross_match_module = CrossMatchingModule()

    def test_successful_query(self):
        result = self.cross_match_module.cross_match(1, '6279435494640163584')
        self.assertIsNotNone(result)
        self.assertFalse(result.empty)

    def test_empty_result_query(self):
        result = self.cross_match_module.cross_match(0, 6279435494640163584)
        self.assertIsNotNone(result)
        self.assertTrue(result.empty)

    def test_invalid_angular_distance(self):
        result = self.cross_match_module.cross_match('lol', 6279435494640163584)
        self.assertIsNone(result)

    def test_invalid_source_id(self):
        result = self.cross_match_module.cross_match(1, 'lol')
        self.assertIsNone(result)

    def test_neg_value_for_angular_distance(self):
    # Check if a ValueError is raised for a negative angular distance
        with self.assertRaises(ValueError):
            self.cross_match_module.cross_match(-1, 123456)

if __name__ == '__main__':
    unittest.main()
