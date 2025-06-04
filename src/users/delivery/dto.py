from pydantic import BaseModel

from src.users.domain.entity import PlainUser


class RegisterUserRequest(BaseModel):
    username: str
    password: str

    def to_entity(self) -> PlainUser:
        return PlainUser(
            username=self.username,
            plain_password=self.password,
        )

class RegisterUserResponse(BaseModel):
    id: int
    username: str


class LoginRequest(BaseModel):
    username: str
    password: str

    def to_entity(self) -> PlainUser:
        return PlainUser(
            username=self.username,
            plain_password=self.password,
        )

class LoginResponse(BaseModel):
    access_token: str
