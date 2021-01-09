import pytest
from datetime import datetime
from pull_fb import url


@pytest.fixture
def tilemovement_res():

    return url.format_urls('TileMovement', '123', [datetime(2000, 1, 1)])


@pytest.fixture
def tilepopulation_res():

    return url.format_urls('TilePopulation', '123', [datetime(2000, 1, 1)])


def test_format_urls_is_list(tilemovement_res):

    assert type(tilemovement_res) is list


def test_format_urls_item_is_dict(tilemovement_res):

    assert type(tilemovement_res[0]) is dict


def test_format_urls_url_is_str(tilemovement_res):

    assert type(tilemovement_res[0]['url']) is str


def test_format_urls_url_tilemovement_has_vector(tilemovement_res):

    assert 'vector' in tilemovement_res[0]['url']


def test_format_urls_url_tilepopulation_has_raster(tilepopulation_res):

    assert 'raster' in tilepopulation_res[0]['url']
