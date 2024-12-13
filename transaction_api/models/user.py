from datetime import datetime
from typing import Annotated, ClassVar

from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr, Field
from pymongo import ASCENDING, IndexModel


class User(BaseModel):
    collection_name: ClassVar = "users"
    indexes: ClassVar[list[list]] = [IndexModel([("user_id", ASCENDING)])]

    id: Annotated[str, BeforeValidator(str)] = Field(alias="_id")
    user_id: str
    name: str
    email: str
    balance: float
    created_at: datetime

    model_config = ConfigDict(populate_by_name=True)


class BaseUser(BaseModel):
    user_id: str = Field(alias="userId")
    name: str
    email: EmailStr


class UserOut(BaseUser):
    created_at: datetime = Field(alias="createdAt")
    model_config = ConfigDict(
        title="User",
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {
                    "userId": "user1",
                    "name": "Alice Smith",
                    "email": "alice@example.com",
                    "createdAt": datetime.now().isoformat(),
                }
            ]
        },
    )


class UserInput(BaseUser):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"userId": "user1", "name": "Alice Smith", "email": "alice@example.com"}]
        }
    )
