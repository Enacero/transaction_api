from datetime import datetime
from typing import Annotated, ClassVar
from pymongo import ASCENDING, IndexModel

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


class Transaction(BaseModel):
    collection_name: ClassVar[str] = "transactions"
    indexes: ClassVar[list[list]] = [
        IndexModel([("timestamp", ASCENDING)]),
        IndexModel([("user_id", ASCENDING)]),
    ]

    id: Annotated[str, BeforeValidator(str)] = Field(alias="_id")
    transaction_id: str
    user_id: str
    amount: float
    timestamp: datetime

    model_config = ConfigDict(populate_by_name=True)


class BaseTransaction(BaseModel):
    transaction_id: str = Field(alias="transactionId")
    user_id: str = Field(alias="userId")
    timestamp: datetime
    amount: float


class TransactionInput(BaseTransaction):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "transactionId": "trxn123",
                    "userId": "user_id",
                    "amount": 123,
                    "timestamp": "2024-12-13T14:17:25.647561",
                }
            ]
        }
    )


class TransactionOut(BaseTransaction):
    model_config = ConfigDict(
        title="Transaction",
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {
                    "transactionId": "a9p3xsdodq24",
                    "userId": "user1",
                    "timestamp": "2024-12-13T13:36:22.482935",
                    "amount": 439.6564024363496,
                }
            ]
        },
    )
