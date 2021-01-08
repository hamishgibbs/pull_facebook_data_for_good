try:
    from pull_fb.pull_fb import credentials
except Exception:
    pass

try:
    from pull_fb import credentials
except Exception:
    pass


def test_credentials_filled():

    res = credentials.get_credentials('a', 'b')

    assert type(res) is dict
