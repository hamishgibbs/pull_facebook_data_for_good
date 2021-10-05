from pull_fb.collection import get_outfn


def test_get_outfn():

    res = get_outfn("1", "a")

    assert res == "a/1.csv.zip"
