from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    user_name: str = Field(..., max_length=40)
    email: EmailStr = Field(..., max_length=50)
    role_id: int


class RegisterRequest(UserBase):
    user_password: str = Field(..., min_length=8,max_length=72)


class LoginRequest(BaseModel):
    email: EmailStr
    user_password: str = Field(..., min_length=8, max_length=72)


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    role_name: Optional[str] = None

class CurrentUserResponse(UserResponse):
    pass


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
