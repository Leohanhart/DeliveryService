from pydantic import BaseModel


class ReturnUserDTO(BaseModel):
    id: int
    username: str
    role: str