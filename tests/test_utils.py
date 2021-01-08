try:
    from pull_fb.pull_fb import utils
except Exception:
    pass

try:
    from pull_fb import utils
except Exception:
    pass


import pytest

from datetime import datetime


# Test date_str_to_datetime
def test_date_str_to_datetime_hours():

    s = "2020_04_30_16"

    res = utils.date_str_to_datetime(s)

    assert type(res) is datetime


def test_date_str_to_datetime_days():

    s = "2020_04_30"

    res = utils.date_str_to_datetime(s)

    assert type(res) is datetime


def test_date_str_to_datetime_errors():

    s = "not a date"

    with pytest.raises(ValueError):

        utils.date_str_to_datetime(s)


@pytest.fixture
def example_date_config():
    return {
        "start_date": datetime(2020, 1, 1),
        "end_date": datetime(2020, 1, 2),
        "frequency": 8,
    }


# Test get_file_dates
def test_get_file_dates_8h(example_date_config):

    res = utils.get_file_dates(
        example_date_config["start_date"], example_date_config["end_date"], 8
    )

    assert len(res) == 3


def test_get_file_dates_12h(example_date_config):

    res = utils.get_file_dates(
        example_date_config["start_date"], example_date_config["end_date"], 12
    )

    assert len(res) == 2


def test_get_file_dates_type(example_date_config):

    res = utils.get_file_dates(
        example_date_config["start_date"], example_date_config["end_date"], 12
    )

    assert type(res[0]) is datetime
