from fastapi import APIRouter, status

from transaction_api.repository import statistics as statistics_repo
from transaction_api.repository.statistics import AccountSummary

from .utils import UserId

router = APIRouter(prefix="/account-summary", tags=["statistics"])


@router.get(
    "/{userId}",
    responses={
        str(status.HTTP_404_NOT_FOUND): {
            "content": {"application/json": {"example": {"detail": "User with id 'user_id' not found"}}}
        }
    },
)
async def get_account_summary(user_id: str = UserId) -> AccountSummary:
    return await statistics_repo.get_account_summary(user_id)
