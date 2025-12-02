from pydantic import BaseModel


class FirebaseUserSchemas(BaseModel):
    uid: str
    email: str
    email_verified: bool
