import os
import tempfile

import pytest

from flaskserver import app
from flaskserver.database import init_db

# request helpers


def deposit(client, acc_no, ass_type, amt):
    return client.post(f'/account/{acc_no}', data=dict(
        asset_type=ass_type,
        deposit_amt=amt
    ))


def withdraw(client, acc_no, ass_type, amt):
    return client.put(f'/account/{acc_no}', data=dict(
        asset_type=ass_type,
        deposit_amt=amt
    ))


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            init_db
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_empty_db(client):
    """Start with a blank database."""

    # get balance of invalid account
    rv = client.get('/account/1')
    assert b'account 1 does not exist' in rv.data

    # deposit to invalid account
    rv = deposit(client, 1, 'BTC', 2.3402)
    assert b'account 1 does not exist' in rv.data

    # withdraw from invalid account
    rv = withdraw(client, 1, 'BTC', 2.3402)
    assert b'account 1 does not exist' in rv.data


def test_deposit(client):
    """create account and deposit different currencies"""

    # create dummy account
    pass


def test_withdrawal(client):
    # create dummy account
    # deposit
    # withdraw
    pass


def test_exchange(client):
    # create dummy account
    # deposit
    # exchange between accounts
    pass


def test_get_balances(client):
    # create dummy account and transactions
    # all balances
    # specific asset
    # assets for certain time interval
    pass
