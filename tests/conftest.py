"""
tests/conftest.py

Adds BACKEND/ to sys.path so all test imports resolve correctly,
and provides the shared flask_client fixture.
"""
import sys
import os
import tempfile

BACKEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'BACKEND')
sys.path.insert(0, os.path.abspath(BACKEND_DIR))

os.environ.setdefault('FLASK_SKIP_DB_INIT', '1')

import pytest


@pytest.fixture
def flask_client():
    """
    Yield a Flask test client backed by an isolated temporary SQLite database.
    """
    import database.db as db_module
    import app as app_module

    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)

    original_path = db_module.DB_PATH
    db_module.DB_PATH = db_path

    db_module.init_db()

    app_module.app.config['TESTING'] = True
    app_module.app.config['SECRET_KEY'] = 'test-secret-key'

    with app_module.app.test_client() as test_client:
        yield test_client

    db_module.DB_PATH = original_path
    os.unlink(db_path)
