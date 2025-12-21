from pydantic import BaseModel, EmailStr


class UserSchemas(BaseModel):
    email: EmailStr
    uid: str
    id: int
    name: str
