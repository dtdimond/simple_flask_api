import pytest
from flask_api import create_app
from flask_api.cache import get_cache, reset_cache


@pytest.fixture
def client():
    app = create_app()
    yield app.test_client()


@pytest.fixture
def init_empty_cache():
    # Fixture to verify cache starts empty
    reset_cache()
    assert not get_cache()

