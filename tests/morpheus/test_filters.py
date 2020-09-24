import unittest
from morpheus.data_loading import DataLoading
from tests import CommonTestSetup
from morpheus.filters import Filter


class FilterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data_path, self.path_prefix = CommonTestSetup.set_data_dir_path()

    def test_filter_dask_dataframe(self):
        data = DataLoading.get_twitter_data_as_bags(self.data_path).to_dataframe()
        results = Filter.filter(rows=data, column_name='lang', like='en')
        self.assertTrue(results.compute().shape[0] != 0)
