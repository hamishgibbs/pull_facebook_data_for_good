import pytest
from pull_fb import utils
from datetime import datetime


@pytest.fixture
def example_date_config():
    return {
        "start_date": datetime(2020, 1, 1),
        "end_date": datetime(2020, 1, 2),
        "frequency": 8,
    }


@pytest.fixture(scope="session")
def local_config_file(tmpdir_factory):

    fn = tmpdir_factory.mktemp("tmp").join(".config")

    with open(fn, 'w') as f:

        f.write('Britain_TileMovement_ID=1671212783027520\nBritain_TileMovement_Origin=2020_03_10_0')

    return fn


@pytest.fixture(scope="session")
def local_config_file_missing_id(tmpdir_factory):

    fn = tmpdir_factory.mktemp("tmp").join(".config")

    with open(fn, 'w') as f:

        f.write('Britain_TileMovement_Origin=2020_03_10_0')

    return fn


@pytest.fixture(scope="session")
def local_config_file_missing_origin(tmpdir_factory):

    fn = tmpdir_factory.mktemp("tmp").join(".config")

    with open(fn, 'w') as f:

        f.write('Britain_TileMovement_ID=1671212783027520')

    return fn


@pytest.fixture(scope="session")
def local_config_file_malformed(tmpdir_factory):

    fn = tmpdir_factory.mktemp("tmp").join(".config")

    with open(fn, 'w') as f:

        f.write('Britain_Colocation_ID=229180671540661Britain_Colocation_Origin=2020_02_11Britain_TilePopulation_ID=881889318900484')

    return fn


@pytest.fixture(scope="session")
def output_csv(tmpdir_factory):

    fn = tmpdir_factory.mktemp("tmp").join("Britain_2020_06_05_1600.csv")

    with open(fn, 'w') as f:

        f.write('test')

    return fn


# Test date_str_to_datetime
def test_date_str_to_datetime_hours():

    s = "2020_04_30_16"

    res = utils.date_str_to_datetime(s)

    assert type(res) is datetime


def test_date_str_to_datetime_days():

    s = "2020_04_30"

    res = utils.date_str_to_datetime(s)

    assert type(res) is datetime


def test_date_str_to_datetime_errors():

    s = "not a date"

    with pytest.raises(ValueError):

        utils.date_str_to_datetime(s)


# Test get_file_dates
def test_get_file_dates_8h(example_date_config):

    res = utils.get_file_dates(
        example_date_config["start_date"], example_date_config["end_date"], 8
    )

    assert len(res) == 3


def test_get_file_dates_12h(example_date_config):

    res = utils.get_file_dates(
        example_date_config["start_date"], example_date_config["end_date"], 12
    )

    assert len(res) == 2


def test_get_file_dates_type(example_date_config):

    res = utils.get_file_dates(
        example_date_config["start_date"], example_date_config["end_date"], 12
    )

    assert type(res[0]) is datetime


# test get_config
def test_get_config_remote():

    path = "https://raw.githubusercontent.com/hamishgibbs/pull_facebook_data_for_good/master/.config"

    res = utils.get_config(path)

    assert type(res) is dict


def test_get_config_local(local_config_file):

    res = utils.get_config(str(local_config_file))

    assert type(res) is dict


def test_get_config_local_raises_malformed(local_config_file_malformed):

    with pytest.raises(Exception):

        utils.get_config(str(local_config_file_malformed))


# test get download variables
def test_get_download_variables_works(local_config_file):

    now = datetime.now()

    res = utils.get_download_variables('TileMovement',
                                       'Britain',
                                       now,
                                       str(local_config_file))

    assert type(res) is dict

    assert res['dataset_id'] == '1671212783027520'

    assert res['start_date'] == datetime(2020, 3, 10, 0)

    assert res['end_date'] == now


def test_get_download_variables_missing_id(local_config_file_missing_id):

    with pytest.raises(KeyError):

        utils.get_download_variables('TileMovement',
                                     'Britain',
                                     datetime.now(),
                                     str(local_config_file_missing_id))


def test_get_download_variables_missing_origin(local_config_file_missing_origin):

    with pytest.raises(KeyError):

        utils.get_download_variables('TileMovement',
                                     'Britain',
                                     datetime.now(),
                                     str(local_config_file_missing_origin))


# test get_existing_dates
def test_get_existing_dates(output_csv):

    outdir = '/'.join(str(output_csv).split('/')[:-1])

    res = utils.get_existing_dates(outdir, 'Britain')

    assert type(res) is list
