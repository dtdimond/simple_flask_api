from datetime import datetime
from unittest.mock import patch


def test_home_page(client, init_empty_cache):
    # Not implemented
    response = client.get('/')
    assert response.status_code == 404
    response = client.put('/')
    assert response.status_code == 404


@patch('flask_api.cache.get_now')
def test_metric_post_and_get_basic(mock_now, client, init_empty_cache):
    now_ret_val = datetime(2021, 6, 1, 10, 0)
    mock_now.return_value = now_ret_val

    # GET with nothing in the cache
    response = client.get('/metric/some_key/sum')
    assert response.status_code == 200
    assert response.json == dict(value=0)

    # POST some data, assert it gets properly rounded and stored for the GET
    response = client.post('/metric/some_key', json={"value": 10.1})
    assert response.status_code == 200
    response = client.get('/metric/some_key/sum')
    assert response.status_code == 200
    assert response.json == dict(value=10)

    # GET - other keys unaffected
    response = client.get('/metric/some_other_key/sum')
    assert response.status_code == 200
    assert response.json == dict(value=0)


@patch('flask_api.cache.get_now')
def test_metric_post_and_get_expired_data(mock_now, client, init_empty_cache):
    mock_now.return_value = datetime(2021, 6, 1, 10, 0)

    # POST some data
    client.post('/metric/some_key', json={"value": 10.1})
    client.post('/metric/some_key', json={"value": -4.8})
    response = client.get('/metric/some_key/sum')
    assert response.json == dict(value=5)

    # Move time forward half an hour and re-check
    mock_now.return_value = datetime(2021, 6, 1, 10, 30)
    response = client.get('/metric/some_key/sum')
    assert response.json == dict(value=5)

    # Move time forward again 30 mins and re-check (edge case)
    mock_now.return_value = datetime(2021, 6, 1, 11, 0)
    response = client.get('/metric/some_key/sum')
    assert response.json == dict(value=5)

    # Move time forward again 1 more min and re-check
    mock_now.return_value = datetime(2021, 6, 1, 11, 1)
    response = client.get('/metric/some_key/sum')
    assert response.json == dict(value=0)


@patch('flask_api.cache.get_now')
def test_metric_bad_post(mock_now, client, init_empty_cache):
    mock_now.return_value = datetime(2021, 6, 1, 10, 0)

    # POST some data
    response = client.post('/metric/some_key', json={"bad_val": 10.1})
    assert response.status_code == 400
