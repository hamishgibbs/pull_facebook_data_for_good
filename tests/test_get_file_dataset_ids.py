import pytest

from pull_fb.collection import get_file_dataset_ids


def test_get_file_dataset_ids():

    files = ["a/b/c/1_2020-01-01_0000.csv"]

    res = get_file_dataset_ids(files)

    assert res == ["1"]


def test_get_file_dataset_ids_raises():

    files = [None]

    with pytest.raises(Exception):
        get_file_dataset_ids(files)
