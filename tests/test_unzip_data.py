import os
import pytest
import shutil
from tests.utils import tmpdir

from pull_fb.collection import unzip_data


def test_unzip_data(tmpdir):

    fn = str(tmpdir + "/123456789123456_2020-01-01_0000.csv")
    zip_fn = fn + ".zip"

    with open(fn, "w") as f:
        f.write("text")

    assert os.path.exists(fn)

    shutil.make_archive(fn, 'zip', tmpdir)

    assert os.path.exists(zip_fn)

    os.remove(fn)

    assert not os.path.exists(fn)

    unzip_data(zip_fn, tmpdir)

    assert os.path.exists(fn)


def test_unzip_data_raises(tmpdir):

    fn = str(tmpdir + "/123456789123456_2020-01-01_0000.csv")
    zip_fn = fn + ".zip"

    with pytest.raises(Exception):
        unzip_data(zip_fn, tmpdir)
