from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Literal, Optional
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


class AdminUserCreate(UserBase):
    role_id: Literal[1, 2, 3]
    user_password: str = Field(..., min_length=8, max_length=72)


class AdminUserUpdate(BaseModel):
    user_name: Optional[str] = Field(None, max_length=40)
    email: Optional[EmailStr] = Field(None, max_length=50)
    role_id: Optional[Literal[1, 2, 3]] = None
    active: Optional[bool] = None


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., min_length=8, max_length=72)
    new_password: str = Field(..., min_length=8, max_length=72)


class PasswordResetRequest(BaseModel):
    new_password: str = Field(..., min_length=8, max_length=72)
