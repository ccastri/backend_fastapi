from pydantic import BaseModel


class UserRegister(BaseModel):
    # id: int
    company: str
    nit: str
    city: str
    department: str
    email: str
    password: str
    password_confirm: str
    role: str
    tos: bool
