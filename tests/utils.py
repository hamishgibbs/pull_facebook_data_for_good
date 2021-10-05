import pytest

@pytest.fixture(scope="session")
def tmpdir(tmpdir_factory):
    tmp = tmpdir_factory.mktemp("data")
    return tmp
