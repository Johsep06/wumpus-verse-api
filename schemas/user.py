from pydantic import BaseModel, EmailStr, Field


class UserSchemas(BaseModel):
    email: EmailStr
    uid: str
    name: str
