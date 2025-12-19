from pydantic import BaseModel, EmailStr, Field


class UserSchemas(BaseModel):
    email: EmailStr
    uid: str
    id: int
    name: str
