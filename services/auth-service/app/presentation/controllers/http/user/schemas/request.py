from pydantic import BaseModel


class UpdateUserRequest(BaseModel):
    username: str
