from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from transaction_api.models.user import UserInput, UserOut
from transaction_api.repository import users as user_repo

from .utils import UserId

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    responses={
        str(status.HTTP_201_CREATED): {
            "content": {
                "application/json": {"example": {"success": True, "message": "User created successfully."}}
            }
        },
        str(status.HTTP_400_BAD_REQUEST): {
            "description": "User already exists",
            "content": {"application/json": {"example": {"detail": "User with id 'user_id' already exists"}}},
        },
    },
    status_code=status.HTTP_201_CREATED,
)
def add_user(user: UserInput):
    user_repo.add_user(user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"success": True, "message": "User created successfully."},
    )


@router.get("")
def get_users() -> list[UserOut]:
    return user_repo.get_all_users()


@router.get(
    "/{userId}",
    responses={
        str(status.HTTP_404_NOT_FOUND): {
            "content": {"application/json": {"example": {"detail": "User with id 'user_id' not found"}}}
        },
    },
)
def get_user(user_id: str = UserId) -> UserOut:
    return user_repo.get_user_by_id(user_id)


@router.delete(
    "/{userId}",
    responses={
        str(status.HTTP_404_NOT_FOUND): {
            "content": {"application/json": {"example": {"detail": "User with id 'user_id' not found"}}}
        },
        str(status.HTTP_200_OK): {
            "content": {
                "application/json": {"example": {"success": True, "message": "User deleted successfully."}}
            }
        },
    },
)
def deleter_user(user_id: str = UserId) -> dict:
    user_repo.delete_user(user_id)
    return {"success": True, "message": "User deleted successfully."}
