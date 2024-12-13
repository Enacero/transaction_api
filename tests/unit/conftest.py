import pytest

from fastapi.testclient import TestClient
from transaction_api.models.user import User
from transaction_api.models.transaction import Transaction

from app import create_app


class FakeDb:
    def __init__(self, mocker):
        self.users_collection = mocker.MagicMock()
        self.transactions_collection = mocker.MagicMock()
        self.database = self
        self.client = mocker.MagicMock()

    def get_collection(self, name):
        if name == User.collection_name:
            return self.users_collection
        if name == Transaction.collection_name:
            return self.transactions_collection


@pytest.fixture(scope="function")
def fake_db(mocker):
    return FakeDb(mocker)


@pytest.fixture(scope="function")
def client(mocker, fake_db):
    mocker.patch("transaction_api.repository.users.db_service", fake_db)
    mocker.patch("transaction_api.repository.transactions.db_service", fake_db)
    mocker.patch("transaction_api.repository.statistics.db_service", fake_db)
    mocker.patch("app.initialize.initialize_indexes")
    app = create_app()
    yield TestClient(app)
