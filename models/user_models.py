from pydantic import BaseModel


class UserRegister(BaseModel):
    # id: int
    company: str
    nit: str
    city: str
    department: str
    username: str
    password: str
    password_confirm: str
    role: str
    tos: bool


class UserLogin(BaseModel):
    username: str
    password: str
