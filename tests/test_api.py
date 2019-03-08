import os
import tempfile

import pytest

# from school_api import
from school_api import app


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        school_api.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])
    '''db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True
    client = flaskr.app.test_client()

    with flaskr.app.app_context():
        flaskr.init_db()

    yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])
    '''


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/students/all')
    assert b'No entries here so far' in rv.data