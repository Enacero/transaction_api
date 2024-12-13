import pytest
from datetime import datetime

from transaction_api.models.transaction import Transaction
from transaction_api.models.user import User
from .conftest import fake_db
from .user_data import test_user_1


@pytest.mark.asyncio
async def test_add_transaction_success(mocker, client, fake_db):
    """
    Test the add_transaction endpoint to ensure a transaction is added successfully
    and the user's balance is updated correctly.
    """
    transaction_data = {
        "transactionId": "txn123",
        "userId": "test123",
        "amount": 100.0,
        "timestamp": "2023-12-12T10:00:00",
    }
    user_data = test_user_1.copy()
    user_data["balance"] = 200

    user_collection = fake_db.database.get_collection(User.collection_name)
    user_collection.find_one.return_value = user_data
    user_collection.update_one = mocker.MagicMock()

    mock_update_balance = user_collection.update_one
    response = client.post("/transactions", json=transaction_data)

    assert response.status_code == 201
    assert response.json() == {"success": True, "message": "Transaction created successfully."}

    mock_update_balance.assert_called_once_with({"user_id": "test123"}, {"$inc": {"balance": 100.0}})


@pytest.mark.asyncio
async def test_add_transaction_insufficient_balance(client, fake_db):
    """
    Test the add_transaction endpoint to ensure a 400 error is returned if the transaction
    would result in a negative balance.
    """
    transaction_data = {
        "transactionId": "txn123",
        "userId": "test123",
        "amount": -300.0,
        "timestamp": "2023-12-12T10:00:00",
    }

    user_data = test_user_1.copy()
    user_data["balance"] = 200
    user_collection = fake_db.database.get_collection(User.collection_name)
    user_collection.find_one.return_value = user_data

    response = client.post("/transactions", json=transaction_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "User with id 'test123' has insufficient balance"}


@pytest.mark.asyncio
async def test_add_transaction_user_not_found(client, fake_db):
    """
    Test the add_transaction endpoint to ensure a 404 error is returned if the userId does not exist.
    """
    transaction_data = {
        "transactionId": "txn123",
        "userId": "nonexistent",
        "amount": 100.0,
        "timestamp": "2023-12-12T10:00:00",
    }
    user_collection = fake_db.database.get_collection(User.collection_name)
    user_collection.find_one.return_value = None

    response = client.post("/transactions", json=transaction_data)

    assert response.status_code == 404
    assert response.json() == {"detail": "User with id 'nonexistent' not found"}


@pytest.mark.asyncio
async def test_list_transactions(client, fake_db):
    """
    Test the list_transactions endpoint to ensure it returns transactions filtered by userId
    and optional date range.
    """
    transactions = [
        {
            "id": "txn123",
            "transaction_id": "txn1",
            "user_id": "user123",
            "amount": 100.0,
            "timestamp": datetime(2023, 12, 10, 10, 0, 0),
        },
        {
            "id": "txn124",
            "transaction_id": "txn2",
            "user_id": "user123",
            "amount": -50.0,
            "timestamp": datetime(2023, 12, 11, 15, 30, 0),
        },
    ]

    transaction_collection = fake_db.database.get_collection(Transaction.collection_name)
    transaction_collection.find.return_value = transactions

    response = client.get("/transactions", params={"userId": "user123"})

    assert response.status_code == 200
    assert response.json() == [
        {"transactionId": "txn1", "userId": "user123", "amount": 100.0, "timestamp": "2023-12-10T10:00:00"},
        {"transactionId": "txn2", "userId": "user123", "amount": -50.0, "timestamp": "2023-12-11T15:30:00"},
    ]
