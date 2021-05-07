import os
import pytest
from tests.utils import tmpdir

from pull_fb.collection import write_zipfile


def test_write_zipfile(tmpdir):

    fn = tmpdir + "/test.zip"
    data = [b"a"]

    write_zipfile(fn, data)

    assert os.path.exists(fn)


def test_write_zipfile_raises(tmpdir):

    fn = tmpdir + "/test.zip"
    data = [None]

    with pytest.raises(Exception):
        write_zipfile(fn, data)
