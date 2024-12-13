from datetime import datetime

from fastapi import HTTPException

from transaction_api.exceptions import UserDoesNotExist
from transaction_api.models.user import User, UserInput, UserOut
from transaction_api.services.database import db_service


def get_user_by_id(user_id: str) -> User:
    user = db_service.database.get_collection(User.collection_name).find_one({"user_id": user_id})
    if not user:
        raise UserDoesNotExist(user_id)

    return User(**user)


def get_all_users() -> list[UserOut]:
    users = db_service.database.get_collection(User.collection_name).find(
        {}, projection={"user_id": 1, "name": 1, "email": 1, "created_at": 1}
    )
    return [UserOut(**user) for user in users]


def user_exists(user_id: str) -> bool:
    user = db_service.database.get_collection(User.collection_name).find_one(
        {"user_id": user_id}, projection={"_id": True}
    )
    return user is not None


def add_user(user: UserInput) -> None:
    if user_exists(user.user_id):
        raise HTTPException(status_code=400, detail=f"User with id '{user.user_id}' already exists")
    db_service.database.get_collection(User.collection_name).insert_one(
        {
            **user.model_dump(),
            "created_at": datetime.now(),
            "balance": 0.0,
        }
    )


def delete_user(user_id: str) -> None:
    if not user_exists(user_id):
        raise UserDoesNotExist(user_id)
    db_service.database.get_collection(User.collection_name).delete_one({"user_id": user_id})


def update_user_balance(user_id: str, amount: float) -> None:
    db_service.database.get_collection(User.collection_name).update_one(
        {"user_id": user_id}, {"$inc": {"balance": amount}}
    )
