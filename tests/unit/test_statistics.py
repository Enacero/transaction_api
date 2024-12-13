import pytest

from transaction_api.models.user import User


@pytest.mark.asyncio
async def test_get_account_summary_success(client, fake_db):
    """Test retrieving account summary for a user."""

    user_id = "user123"
    account_summary_data = {"userId": user_id, "currentBalance": 200.0, "transactionCount": 5}

    fake_db.database.get_collection(User.collection_name).aggregate.return_value.try_next.return_value = (
        account_summary_data
    )

    response = client.get(f"/account-summary/{user_id}")

    assert response.status_code == 200
    assert response.json() == account_summary_data


def test_get_account_summary_user_not_found(client, fake_db):
    """Test retrieving account summary when user does not exist."""

    user_id = "nonexistent"

    fake_db.database.get_collection(User.collection_name).aggregate.return_value.try_next.return_value = None

    response = client.get(f"/account-summary/{user_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"User with id '{user_id}' not found"}
