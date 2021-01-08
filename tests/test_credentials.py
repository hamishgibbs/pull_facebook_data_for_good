try:
    from pull_fb.pull_fb import credentials
except Exception:
    pass

from pull_fb import credentials


def test_credentials_filled():

    res = credentials.get_credentials('a', 'b')

    assert type(res) is dict
