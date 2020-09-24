import unittest
from dask.bag import Bag
from Morpheus.data_loading import DataLoading
from glob import glob


class DataLoadingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        try:
            self.data_path = '../../data/*.json.bz2'
            self.path_prefix = '../../data'
            assert glob(self.data_path) == ['../../data\\test_sample_files.json.bz2',
                                            '../../data\\test_sample_files_2.json.bz2']
        except AssertionError:
            self.data_path = 'data/*.json.bz2'
            self.path_prefix = 'data'
            print(glob(self.data_path))

    def test_get_files_list_in_data(self):
        self.assertEqual(
            DataLoading.get_files_list(self.data_path), [f'{self.path_prefix}\\test_sample_files.json.bz2',
                                                         f'{self.path_prefix}\\test_sample_files_2.json.bz2'])

    def test_get_files_list_when_no_files_present(self):
        try:
            DataLoading.get_files_list('../../data/no-files.abcd')
            self.assertFalse(False)
        except ValueError:
            self.assertTrue(True)

    def test_read_compressed_bz2_json_file(self):
        data = DataLoading.read_compressed_bz2_json_file(f'{self.path_prefix}/test_sample_files.json.bz2')
        self.assertEqual(type(data), list)

    def test_read_compressed_bz2_json_file_when_not_json_bz2_file(self):
        try:
            DataLoading.read_compressed_bz2_json_file('../../data/test_sample_files.json')
            self.assertFalse(False)
        except ValueError:
            self.assertTrue(True)

    def test_get_twitter_data_as_bags(self):
        data = DataLoading.get_twitter_data_as_bags('../../data/test_sample_files.json.bz2')
        self.assertEqual(type(data), Bag)
