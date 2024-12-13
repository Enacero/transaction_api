from datetime import date

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field

from transaction_api.models.transaction import TransactionInput, TransactionOut
from transaction_api.repository import transactions as transaction_repo

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        str(status.HTTP_201_CREATED): {
            "content": {
                "application/json": {
                    "example": {"success": True, "message": "Transaction created successfully."}
                }
            },
        },
        str(status.HTTP_400_BAD_REQUEST): {
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_balance": {
                            "summary": "User Has insufficient balance",
                            "value": {"detail": "User with id 'user_id' has insufficient balance"},
                        },
                        "invalid_user": {
                            "summary": "User does not exist",
                            "value": {"detail": "User with id 'user_id' not found"},
                        },
                    }
                }
            }
        },
    },
)
def add_transaction(transaction: TransactionInput) -> dict:
    transaction_repo.add_transaction(transaction)
    return {"success": True, "message": "Transaction created successfully."}


class TransactionFilters(BaseModel):
    user_id: str = Field(Query(..., alias="userId"))
    start_date: date | None = Field(Query(None, alias="startDate"))
    end_date: date | None = Field(Query(None, alias="endDate"))


@router.get("")
def list_transactions(
    filters: TransactionFilters = Depends(),
) -> list[TransactionOut]:
    return transaction_repo.get_all_transactions(**filters.model_dump())
