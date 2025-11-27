from pydantic import BaseModel, EmailStr, Field


class UserCreateSchemas(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6,
                          description="Senha deve ter pelo menos 6 caracteres")
    name: str = Field(..., min_length=2, max_length=100)
