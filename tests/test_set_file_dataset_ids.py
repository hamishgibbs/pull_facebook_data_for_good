import os
from tests.utils import tmpdir
from pull_fb.collection import set_file_dataset_ids


def test_set_file_dataset_ids(tmpdir):

    fn = str(tmpdir + "/123456789123456_2020-01-01_0000.csv")

    with open(fn, "w") as f:
        f.write("text")

    assert os.path.exists(fn)

    set_file_dataset_ids([fn], "123")

    fn_exp = tmpdir + "/123_2020-01-01_0000.csv"

    assert os.path.exists(
        str(fn_exp)
    )

    os.remove(fn_exp)
