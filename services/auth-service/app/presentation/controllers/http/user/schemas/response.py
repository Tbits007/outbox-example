from pydantic import BaseModel


class UserResponse(BaseModel):
    email: str
    username: str
