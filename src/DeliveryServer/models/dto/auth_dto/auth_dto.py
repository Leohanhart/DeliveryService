from pydantic import BaseModel


class LoginDTO(BaseModel):
    username: str
    password: str

class RegisterDTO(BaseModel):
    username: str
    password: str