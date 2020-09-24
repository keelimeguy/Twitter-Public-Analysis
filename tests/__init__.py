import io
import sys
from glob import glob
from typing import Tuple
from os import path


class CommonTestSetup:
    @staticmethod
    def set_data_dir_path() -> Tuple[str, str]:
        try:
            data_path = '../../data/*.json.bz2'
            path_prefix = '../../data'
            assert glob(data_path) == [path.join(path_prefix, 'test_sample_files.json.bz2'),
                                       path.join(path_prefix, 'test_sample_files_2.json.bz2')]
            return data_path, path_prefix

        except AssertionError:
            path_prefix = 'data'
            data_path = 'data/*.json.bz2'
            return data_path, path_prefix


# Suppress printing to console while running tests
sys.stdout = io.StringIO()
