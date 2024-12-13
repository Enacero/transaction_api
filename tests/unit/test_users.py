import pytest
from datetime import datetime
from freezegun import freeze_time

from transaction_api.models.user import User
from .user_data import test_user_1, test_user_1_json, test_user_2, test_user_2_json


@pytest.mark.asyncio
async def test_add_user_success(mocker, client, fake_db):
    """Test adding a new user successfully.

    Ensures the endpoint responds with success when a user does not already exist
    and is correctly added to the database.
    """
    user_data = test_user_1_json

    user_collection = fake_db.database.get_collection(User.collection_name)
    user_collection.find_one.return_value = None

    mock_insert = mocker.MagicMock()
    user_collection.insert_one = mock_insert

    with freeze_time(datetime.fromisoformat(test_user_1["created_at"])):
        response = client.post("/users", json=user_data)

    assert response.status_code == 201, response.text
    assert response.json() == {"success": True, "message": "User created successfully."}

    expected_data = test_user_1.copy()
    expected_data.pop("_id")
    expected_data["created_at"] = datetime.fromisoformat(expected_data["created_at"])

    mock_insert.assert_called_once_with(expected_data)


@pytest.mark.asyncio
async def test_add_user_already_exists(client, fake_db):
    """Test attempting to add a user that already exists.

    Verifies the endpoint returns a 400 error when trying to add a user
    with an existing ID in the database.
    """
    user_data = test_user_1_json
    user_collection = fake_db.database.get_collection(User.collection_name)
    user_collection.find_one.return_value = {"_id": "existing_id"}

    response = client.post("/users", json=user_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "User with id 'user1' already exists"}


@pytest.mark.asyncio
async def test_add_user_invalid_email(client):
    """
    Test to ensure that the add_user endpoint validates the email format.

    This test attempts to create a user with an invalid email address and verifies
    that the endpoint returns a 422 Unprocessable Entity error. The test also checks
    that the error message specifically mentions the invalid email format, ensuring
    proper validation logic.
    """
    user_data = test_user_1_json.copy()
    user_data["email"] = "invalid-email.com"
    response = client.post("/users", json=user_data)

    assert response.status_code == 422
    assert "email" in response.json()["detail"][0]["loc"]
    assert (
        response.json()["detail"][0]["msg"]
        == "value is not a valid email address: An email address must have an @-sign."
    )


@pytest.mark.asyncio
async def test_get_users(client, fake_db):
    """Test retrieving a list of users.

    Ensures the endpoint returns all users from the database correctly.
    """
    mock_users = [test_user_1, test_user_2]
    user_collection = fake_db.database.get_collection(User.collection_name)
    user_collection.find.return_value = mock_users

    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == [
        test_user_1_json,
        test_user_2_json,
    ]


@pytest.mark.asyncio
async def test_get_user_by_id(client, fake_db):
    """Test retrieving a user by their ID.

    Verifies the endpoint returns the correct user details when the user exists.
    """
    mock_user = test_user_1
    user_collection = fake_db.database.get_collection(User.collection_name)
    user_collection.find_one.return_value = mock_user

    response = client.get("/users/user1")

    assert response.status_code == 200, response.text
    assert response.json() == test_user_1_json


@pytest.mark.asyncio
async def test_get_user_not_found(client, fake_db):
    """Test retrieving a non-existent user by ID.

    Ensures the endpoint returns a 404 error if the user does not exist in the database.
    """
    user_collection = fake_db.database.get_collection(User.collection_name)
    user_collection.find_one.return_value = None

    response = client.get("/users/nonexistent")

    assert response.status_code == 404
    assert response.json() == {"detail": "User with id 'nonexistent' not found"}


@pytest.mark.asyncio
async def test_delete_user_success(client, fake_db):
    """Test deleting an existing user.

    Verifies the endpoint successfully deletes a user when the user exists in the database.
    """
    user_collection = fake_db.database.get_collection(User.collection_name)
    user_collection.find_one.return_value = {"_id": "existing_id"}
    user_collection.delete_one.return_value = None

    response = client.delete("/users/user1")

    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "User deleted successfully."}


@pytest.mark.asyncio
async def test_delete_user_not_found(client, fake_db):
    """Test deleting a non-existent user.

    Ensures the endpoint returns a 404 error if the user to be deleted does not exist.
    """
    user_collection = fake_db.database.get_collection(User.collection_name)
    user_collection.find_one.return_value = None

    response = client.delete("/users/nonexistent")

    assert response.status_code == 404
    assert response.json() == {"detail": "User with id 'nonexistent' not found"}
