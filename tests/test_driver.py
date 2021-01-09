from datetime import datetime
from pull_fb import driver
from selenium import webdriver

def test_format_out_fn():

    res = driver.format_out_fn('a', 'b', datetime(2000, 1, 1, 0))

    assert res == 'a/b_2000_01_01_0000.csv'
