from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=32, description="Username must be 3-50 characters long")
    password: str = Field(min_length=8, max_length=32, description="Password must be 8-50 characters long")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32, description="Password must be 8-50 characters long")


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirmRequest(BaseModel):
    token: str
    new_password: str
