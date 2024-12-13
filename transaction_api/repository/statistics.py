from pydantic import BaseModel, ConfigDict, Field

from transaction_api.exceptions import UserDoesNotExist
from transaction_api.models.transaction import Transaction
from transaction_api.models.user import User
from transaction_api.services.database import db_service


class AccountSummary(BaseModel):
    user_id: str = Field(alias="userId")
    balance: float = Field(alias="currentBalance")
    transaction_count: int = Field(alias="transactionCount")
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={"examples": [{"userId": "user_id", "balance": 100.1, "transaction_count": 10}]},
    )


def get_account_summary(user_id: str) -> AccountSummary:
    summary = (
        db_service.database.get_collection(User.collection_name)
        .aggregate(
            pipeline=[
                {"$match": {"user_id": user_id}},
                {
                    "$lookup": {
                        "from": Transaction.collection_name,
                        "localField": "user_id",
                        "foreignField": "user_id",
                        "as": "transactions",
                    }
                },
                {"$addFields": {"transaction_count": {"$size": "$transactions"}}},
                {"$unset": ["transactions"]},
            ]
        )
        .try_next()
    )
    if not summary:
        raise UserDoesNotExist(user_id)
    return AccountSummary(**summary)
