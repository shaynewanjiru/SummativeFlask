
import pytest
from app import app as flask_app
from tests.helpers import reset_database, seed_inventory

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c

@pytest.fixture(autouse=True)
def fresh_database():
    """Reset database before EVERY test automatically."""
    reset_database(seed_data=seed_inventory())
    yield
    reset_database()