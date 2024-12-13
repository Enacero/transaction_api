from fastapi import HTTPException


class UserDoesNotExist(HTTPException):
    def __init__(self, user_id: str, status_code: int = 404):
        super().__init__(status_code, detail=f"User with id '{user_id}' not found")
