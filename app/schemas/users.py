from typing import Any

from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str

    def model_post_init(self, context: Any, /) -> None:  # noqa: ANN401
        self.email = self.email.lower()


class User(BaseModel):
    id: int
    email: EmailStr
