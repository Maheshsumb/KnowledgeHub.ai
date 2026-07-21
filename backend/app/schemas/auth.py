from uuid import UUID
from pydantic import BaseModel, EmailStr,Field, model_validator


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
class LogoutRequest(BaseModel):
    refresh_token: str