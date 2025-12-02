from pydantic import BaseModel, EmailStr


class UserLoginSchemas(BaseModel):
    email: EmailStr
    password: str
