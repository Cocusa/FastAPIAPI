from os import getenv
import fdb
from fastapi.testclient import TestClient

from .main import app
from .dependencies import get_db


def override_get_db():
    try:
        dbcon = fdb.connect(
            getenv('TEST_DSN'),
            getenv('TEST_USER'),
            getenv('TEST_PASS'),
            charset='utf-8',
            role=getenv('TEST_ROLE'))
        yield dbcon
    finally:
        dbcon.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
