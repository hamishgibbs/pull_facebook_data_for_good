from pull_fb import credentials


def test_credentials_filled():

    res = credentials.get_credentials('a', 'b')

    assert type(res) is dict


def test_credentials_usenrame_none(monkeypatch):

    monkeypatch.setattr('builtins.input', lambda _: "example@gmail.com")

    # go about using input() like you normally would:
    res = credentials.get_credentials(None, 'b')

    assert type(res) is dict
    assert res['email'] == "example@gmail.com"
