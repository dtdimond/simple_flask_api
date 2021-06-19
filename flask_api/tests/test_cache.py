from unittest.mock import patch
from pytest import fixture
from datetime import datetime, timedelta
from flask_api.cache import cache_item, get_from_cache, get_cache


@fixture
def setup_old_data():
    # Fixture to setup some old cache data for a few keys, most recent last
    get_cache()["example"] = [
        (datetime(2021, 5, 1, 10, 0), 1),
        (datetime(2021, 6, 1, 7, 59), 2),
        (datetime(2021, 6, 1, 8, 0), 3),  # this and below will be kept
        (datetime(2021, 6, 1, 9, 0), 4),
    ]
    get_cache()["some_other_key"] = [(datetime(2021, 5, 1, 10, 0), 8)]
    get_cache()["some_other_key2"] = [(datetime(2021, 6, 1, 10, 0), 9)]


@patch('flask_api.cache.get_now')
def test_cache_item_basic(mock_now, init_empty_cache):
    now_ret_val = datetime(2021, 6, 1, 10, 0)
    mock_now.return_value = now_ret_val

    # Cache a few things with custom delete_older_than
    cache_item("example", 1, delete_older_than=timedelta(hours=2))
    cache_item("example2", 2, delete_older_than=timedelta(hours=2))

    assert get_cache().get("example") == [(now_ret_val, 1)]
    assert get_cache().get("example2") == [(now_ret_val, 2)]
    assert get_cache().get("example3") is None


@patch('flask_api.cache.get_now')
def test_cache_item_deletes_old(mock_now, init_empty_cache, setup_old_data):
    now_ret_val = datetime(2021, 6, 1, 10, 0)
    mock_now.return_value = now_ret_val

    # Cache am item for example
    cache_item("example", 0, delete_older_than=timedelta(hours=2))
    cache_item("some_other_key2", 2.2, delete_older_than=timedelta(hours=2))

    # Only most recent item and those less than 2hrs old are maintained
    assert get_cache().get("example") == [
        (datetime(2021, 6, 1, 8, 0), 3),
        (datetime(2021, 6, 1, 9, 0), 4),
        (now_ret_val, 0),
    ]
    assert get_cache().get("some_other_key2") == [
        (datetime(2021, 6, 1, 10, 0), 9),
        (now_ret_val, 2.2),
    ]
    # Other keys untouched
    assert get_cache().get("some_other_key") == [
        (datetime(2021, 5, 1, 10, 0), 8)
    ]
    assert get_cache().get("example3") is None


def test_get_from_cache(init_empty_cache):
    new_val = [(datetime(2021, 5, 1, 10, 0), 8)]
    get_cache()["some_key"] = new_val
    assert get_from_cache("some_key", timedelta(hours=2)) == new_val


@patch('flask_api.cache.get_now')
def test_get_from_cache_deletes_old(
    mock_now, init_empty_cache, setup_old_data
):
    now_ret_val = datetime(2021, 6, 1, 10, 0)
    mock_now.return_value = now_ret_val

    assert not get_from_cache("some_other_key", timedelta(hours=2))
