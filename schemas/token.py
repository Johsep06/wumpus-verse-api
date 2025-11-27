from pydantic import BaseModel, EmailStr, Field

from .user_response import UserResponseSchemas


class TokenSchemas(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponseSchemas
