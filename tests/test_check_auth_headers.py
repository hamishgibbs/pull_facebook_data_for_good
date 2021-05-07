from pull_fb.auth import check_auth_headers


def test_check_auth_headers_true():

    headers = {
        "x-fb-rlafr": "test"
    }

    assert check_auth_headers(headers, "a")


def test_check_auth_headers_false():

    headers = {}

    assert not check_auth_headers(headers, "a")
