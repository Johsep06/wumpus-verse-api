from pydantic import BaseModel, EmailStr


class UserEmailSchemas(BaseModel):
    email: EmailStr