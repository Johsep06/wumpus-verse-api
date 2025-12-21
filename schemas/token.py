from pydantic import BaseModel

from .user_response import UserResponseSchemas


class TokenSchemas(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponseSchemas
