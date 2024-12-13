from datetime import date, datetime, time

from fastapi import HTTPException

from transaction_api.exceptions import UserDoesNotExist
from transaction_api.models.transaction import (
    Transaction,
    TransactionInput,
    TransactionOut,
)
from transaction_api.services.database import db_service

from . import users as user_repo


async def add_transaction(transaction: TransactionInput) -> None:
    if not (user := await user_repo.get_user_by_id(transaction.user_id)):
        raise UserDoesNotExist(transaction.user_id, 400)

    if user.balance + transaction.amount < 0:
        raise HTTPException(
            status_code=400,
            detail=f"User with id '{transaction.user_id}' has insufficient balance",
        )
    with db_service.client.start_session() as session:
        with session.start_transaction():
            db_service.database.get_collection(Transaction.collection_name).insert_one(
                transaction.model_dump()
            )
            await user_repo.update_user_balance(transaction.user_id, transaction.amount)


async def get_all_transactions(
    user_id: str, start_date: date | None = None, end_date: date | None = None
) -> list[TransactionOut]:
    filters = {"user_id": {"$eq": user_id}}
    if start_date or end_date:
        filters["timestamp"] = {}
        if start_date:
            filters["timestamp"]["$gte"] = datetime.combine(start_date, time())
        if end_date:
            filters["timestamp"]["$lt"] = datetime.combine(end_date, time())
    return [
        Transaction(**transaction)
        for transaction in db_service.database.get_collection(Transaction.collection_name).find(filters)
    ]
