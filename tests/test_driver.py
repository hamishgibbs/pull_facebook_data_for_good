import pytest
from datetime import datetime
from pull_fb import driver
from selenium import webdriver
import pandas as pd


@pytest.fixture()
def sample_csv_response():

    return 'a,b\n1,2\n3,4'


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
