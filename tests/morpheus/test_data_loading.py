import unittest
from dask.bag import Bag
from morpheus.data_loading import DataLoading
from tests import CommonTestSetup


class DataLoadingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data_path, self.path_prefix = CommonTestSetup.set_data_dir_path()

    def test_get_files_list_in_data(self):
        """
        Note:
            function assumes that order doesn't matter
            If order matters, glob might have to be reconfigured
        :return:
        """
        self.assertTrue(
            set(DataLoading.get_files_list(self.data_path)) == {f'{self.path_prefix}\\test_sample_files.json.bz2',
                                                                f'{self.path_prefix}\\test_sample_files_2.json.bz2'})

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

        def test_remove_deleted_tweets(self):
            """
            Note: Function assumes that there is a removed tweet in the first 20 tweets.
            :return:
            """
            bags = DataLoading.get_twitter_data_as_bags(self.data_path, remove_deleted_tweets=False)
            removed_tweets = DataLoading.remove_deleted_tweets(bags)
            bags = bags.take(20)
            computed = removed_tweets.take(20)
            self.assertNotEqual(bags, computed)
