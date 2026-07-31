"""
Pydantic schemas for Authentication and Token generation data handling.
"""

from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    """
    Schema validating login attempts.
    """
    email: EmailStr = Field(..., description="Registered user email identity credential field")
    password: str = Field(..., description="Plaintext security challenge sequence parameter")

class Token(BaseModel):
    """
    Schema for access token responses rendered in successful logins.
    """
    access_token: str = Field(..., description="The JWT bearer access token string")
    token_type: str = Field("bearer", description="The token string transport wrapper format type")


class TokenData(BaseModel):
    """
    Internal token verification metadata container.
    """
    email: str | None = Field(None, description="The specific user context identifier extracted from the JWT payload claims")

