from typing import Any

from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str


class UserCredentials(BaseModel):
    email: EmailStr
    password: str

    def model_post_init(self, context: Any, /) -> None:  # noqa: ANN401
        self.email = self.email.lower()


class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str

    def model_post_init(self, context: Any, /) -> None:  # noqa: ANN401
        self.email = self.email.lower()


class UserGet(BaseModel):
    id: int
    email: EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
