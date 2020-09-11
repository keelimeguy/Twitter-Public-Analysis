import dask
import dask.bag as db
import json
import bz2
from typing import List


def _read_compressed_bz2_json_file(file_path: str) -> List[dict]:
    """
    Read a compressed bz2 json file. Best used when you have a list of json files
    :param file_path: path of the file that needs to be read
    :return: List of json like dictionaries that contain information on tweets
    """
    if 'json.bz2' not in file_path:
        raise ValueError('File Passed is not json.bz2 file')
    file = bz2.open(file_path)
    data = file.read().decode("utf-8").split('\n')[:-1]
    return [json.loads(tweet) for tweet in data]


def _read_compressed_bz2_json_text(file_contents: str):
    """
    create json data from compressed bz2 text.
    Note: dask.bags.read_text might already uncompress this data, hence compression has been skipped here
    :param file_contents: text that is in a json/dict string
    :return: List of json like dictionaries that contain information on tweets
    """
    data = json.loads(file_contents)
    return data


def get_twitter_data_as_bags(file_find_expression='../../data/*.json.bz2') -> dask.bag:
    """
    function to get twitter data as dask bags based on the given directory
    :param file_find_expression: unix like expression for finding the relevant files
    :return: dask bag that contains information on the tweets
    """
    bags = db.read_text(file_find_expression).map(_read_compressed_bz2_json_text)
    return bags


if __name__ == '__main__':
    pass
