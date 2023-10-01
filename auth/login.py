from fastapi import (
    FastAPI,
    Request,
    APIRouter,
    HTTPException,
    File,
    UploadFile,
    Form,
    Depends,
)
from pydantic import BaseModel
from typing import Union

# !
from models.user_models_db import create_user
from models.user_models import UserRegister, UserLogin

#! Import the fastapi dependency for handling OAUTH 2.0 protocol
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

#! Router config
router = APIRouter(tags=["auth"])
# ! I'm going to declare the endpoint that the front end will look For the getting
# ! Authentication to the user. Makes fast api know it is a security scheme
# ! (Checking the headers in the request for the Authorization atribute to be 'Bearer':'token')
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


fake_users_db = {
    "johndoe": {
        "username": "Yannix",
        "full_name": "Yan Murillo",
        "email": "ycm@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


class Login_User:
    username: str
    password: str


# class UserInDB(User):
#     hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# ! OAuth2PasswordRequestForm is just like defining a regular Form class in fastApi
# ! But it is provided by the framework for simplicity


# ! This is going to be the endpoint used by React to send the email and password
# ! from the login form in the frontend
@router.post("/token")
async def token_generate(user_login: OAuth2PasswordRequestForm = Depends()):
    # !Verificar que el usuario existe (usando el correo enviado desde el forntend)
    # # user_dict = fake_users_db.get(form_data.username)
    # if not user_dict:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    # ! Cuando el usuario existe se van a traer todos los atributos del registro en
    # ! la BBDD y se construye la instancia del usuario en sesion
    # user = UserInDB(**user_dict)
    # ! Por ultimo se comparan la contraseña enviada desde el frontend con la contraseña
    # ! hasheada desde el registro en la base de datos. Si no coinciden error 400
    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    # ! Cuando coinciden se devuelve el username del usuario en sesion
    # ! The only thing must be done exactly this way, to be compliant with the specifications.
    # ! For the rest, FastAPI handles it for you.
    return {"access_token": user_login.username, "token_type": "Bearer"}


@router.post("/login")
def read_root(token: str = Depends(oauth_scheme)):
    print(token)
    return {"username": "klk manito", "password": "123456"}


@router.post("/register", status_code=201)
async def create_user_route(user_data: UserRegister):
    try:
        new_user = create_user(user_data)
        return new_user
    except Exception as e:
        error_message = f"Error al procesar los datos: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
