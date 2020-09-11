"""
author: v2thegreat (v2thegreat@gmail.com)

Functions to filter out irrelevant tweets that might not be wanted for processing

TODO:
    - This package is written with the hopes to better understand what problems processing such a dataset would be
    encountered, and it is hence written with the understanding that this and other scripts will be refactored
    - Add tests
"""

from typing import Union, List, Dict, Any, Tuple
import pandas as pd
import dask.dataframe as dask_dataframe
import warnings


class Filter:
    def __init__(self, column_name: str = None, like: Any = None):
        """
        Create Filter object that can filter out unneeded rows
        :param column_name: name of the column to match against
        :param like: what the object is supposed to look like when converted to a string
        """

        self._column_name: str = column_name
        self._like: Any = like

    def _set_column_name_and_like(self, column_name: str = None, like: Any = None) -> Tuple[str, Any]:
        """
        Function to set column_name and like internally.
        If they have not been defined in the class, `ValueError` is raised

        :param column_name:
        :param like:
        :return:
        """
        _column_name = column_name if column_name else self._column_name
        _like = like if like else self._like

        if not _column_name or not _like:
            raise ValueError(f'column_name or like has not been defined in this object or in this function. '
                             f'Please define them and try again')
        return _column_name, _like

    def filter(self, rows: Union[List[Dict], Dict[str, List], pd.DataFrame], column_name: str = None,
               like: Any = None, verbosity: bool = False) -> Union[Dict, List]:
        """
        Function to filter out rows that don't match.

        :param rows: rows that need to be filtered out
        :param column_name: name of the column to match against
        :param like: what the object is supposed to look like when converted to a string
        :param verbosity: Display usage information
        :return:
        """

        _column_name, _like = self._set_column_name_and_like(column_name=column_name, like=like)

        if type(rows) == dict:
            return self._filter_dict(rows=rows, key_name=_column_name, like=_like, verbosity=verbosity)

        if type(rows) == list:
            return self._filter_list(rows=rows, key_name=_column_name, like=_like, verbosity=verbosity)

    def _filter_list(self, rows: List[Dict], key_name: str, like: Any, verbosity: bool) -> Dict:
        """
        Function to filter out rows in the dictionary. Matches against the list in rows[key_name]

        Uses pandas internally to speed things up
        :param rows: rows of data that contains the information that we're looking for
        :param key_name: name of the column to match against
        :param like: value that row needs to be compared to
        :param verbosity: verbosity level
        :return:
        """

        _key_name, _like = self._set_column_name_and_like(column_name=key_name, like=like)

        if verbosity:
            warnings.warn(NotImplemented, 'verbosity has not been implemented for this function at this time')

        df = pd.DataFrame(rows)
        return df[df[_key_name] == _like].to_json()

    def _filter_dict(self, rows: Dict[str, List], key_name: str, like: Any, verbosity: bool) -> Dict:
        """
        Function to filter out rows in the dictionary. Matches against the list in rows[key_name]

        Uses pandas internally to speed things up
        :param rows: rows of data that contains the information that we're looking for
        :param key_name: name of the column to match against
        :param like: value that row needs to be compared to
        :param verbosity: verbosity level
        :return:
        """

        _key_name, _like = self._set_column_name_and_like(column_name=key_name, like=like)

        if verbosity:
            warnings.warn(NotImplemented, 'verbosity has not been implemented for this function at this time')

        df = pd.DataFrame(rows)
        return df[df[_key_name] == _like].to_dict()


if __name__ == "__main__":
    data_dict = {
        'fruits': ['Apples', 'Oranges', 'Tomatoes', 'Apples'],
        'names': ['Amy', 'John', 'Alex', 'Sokka']
    }

    data_list = [
        {'fruits': 'Apples', 'names': 'Amy'},
        {'fruits': 'Oranges', 'names': 'John'},
        {'fruits': 'Tomatoes', 'names': 'Alex'},
        {'fruits': 'Apples', 'names': 'Sokka'}
    ]

    filter_obj = Filter(column_name='fruits', like='Apples')
    assert filter_obj.filter(data_dict) == {'fruits': {0: 'Apples', 3: 'Apples'}, 'names': {0: 'Amy', 3: 'Sokka'}}
    print(filter_obj.filter(data_list))
    assert filter_obj.filter(data_list) == {'fruits': {0: 'Apples', 3: 'Apples'}, 'names': {0: 'Amy', 3: 'Sokka'}}
    print('All Passed!')
