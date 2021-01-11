import os
import pytest
from datetime import datetime
from pull_fb import driver
import requests
import pandas as pd


@pytest.fixture()
def sample_csv_response():

    return 'a,b\n1,2\n3,4'


@pytest.fixture()
def mock_csv_response():

    class Mock_Response():

        def __init__(self):

            self.status_code = 200
            self.text = 'a,b\n1,2\n3,4'

    return Mock_Response()


@pytest.fixture(scope="session")
def tmp_path(tmpdir_factory):

    path = tmpdir_factory.mktemp("tmp")

    return path


def test_format_out_fn():

    res = driver.format_out_fn('a', 'b', datetime(2000, 1, 1, 0))

    assert res == 'a/b_2000_01_01_0000.csv'


def test_response_as_dataframe_reads_csv(sample_csv_response):

    res = driver.response_as_dataframe(sample_csv_response)

    assert type(res) is pd.DataFrame


def test_response_as_dataframe_raises_one_row():

    with pytest.raises(AssertionError):

        driver.response_as_dataframe('a,b\n1,2')


def test_response_as_dataframe_fails_html():

    with pytest.raises(AssertionError):

        driver.response_as_dataframe('<div>Other stuff</div>')


def test_authenticate_session_with_cookies():

    request_cookies_browser = [{'name': 'item', 'value': 'item'}]

    res = driver.authenticate_session(request_cookies_browser)

    assert type(res) is requests.Session


def test_write_outfile(mock_csv_response):

    res = driver.write_outfile(mock_csv_response, 'test.csv', [])

    assert type(res) is list

    os.remove('test.csv')


# test download_data
def test_download_data_tmp_dir(tmp_path):

    download_urls = [{"url": "https://github.com/hamishgibbs/uk_tier_data/raw/master/output/uk_tier_data_parliament_2020_10_25_1606.csv",
                     "date": datetime(2020, 3, 1, 0)}]

    driver.download_data(download_urls,
                         "Britain",
                         str(tmp_path),
                         [])

    assert os.path.exists(str(tmp_path) + '/Britain_2020_03_01_0000.csv')
