import pytest
from datetime import datetime

from pull_fb.collection import get_file_dates


def test_get_file_dates_ids():

    files = ["a/b/c/1_2020-01-01_0000.csv"]

    res = get_file_dates(files)

    assert res == [datetime(2020, 1, 1)]


def test_get_file_dates_raises():

    files = [None]

    with pytest.raises(Exception):
        get_file_dates(files)
