import uvicorn
import os
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from hoja_de_vida import hdv

# from middlewares import upload_image

# from auth import login
import users
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

# from google_quickstart import Create_Service

load_dotenv()
app = FastAPI(docs_url="/docs", openapi_url="/api/openapi.json", debug=False)
app.mount("/static", StaticFiles(directory="static"), name="static")
# encoded_url = os.environ.get("NEXT_PUBLIC_VERCEL_URL")
# decoded_url = urllib.parse.unquote(encoded_url)

# Cors enabled to receive http request from nextjs frontend
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ! Link it with google drive api
# CLIENT_SECRET_FILE = "credentials_oauth.json"
# API_NAME = "drive"
# API_VERSION = "v3"
# SCOPES = ["https://www.googleapis.com/auth/drive"]

# service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
# print(dir(service))


# Trial fastapi model
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


app.include_router(hdv.router)
# app.include_router(upload_image.router)
app.include_router(users.router)
# app.include_router(login.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/hola")
def read_root():
    return {"Hello": "World"}


# at last, the bottom of the file/module
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
# {
#     "departamento": "scssd",
#     "municipio": "un valor",
#     "entidad": "un valor",
#     "correo": "un valor",
#     "direccion": "un valor",
#     "telefono": "un valor",
# }

# {
#     "departamento": "scssd",
#     "municipio": "un valor",
#     "entidad": "un valor",
#     "correo": "un valor",
#     "direccion": "un valor",
#     "telefono": "un valor",
# }
#   "equipo": "un valor",
#   "marca": "un valor",
#   "modelo": "un valor",
#   "serie": "un valor",
#   "activoFijo": "un valor",
#   "registroSanitario": "un valor",
#   "ubicacion": "un valor",
#   "proveedor": "un valor",
#   "img": "un valor",
#   "AdquisitionWay": "un valor",
#   "yearOfFabrication": "2023-08-10",
#   "boughtDate": "2023-08-10",
#   "installationDate": "2023-08-10",
#   "warrantyEnd": "2023-08-10",
#   "fabricante": "un valor",
#   "tension": "un valor",
#   "potencia": "un valor",
#   "presion": "un valor",
#   "corriente": "un valor",
#   "frecuencia": "un valor",
#   "rangoTemperatura": "un valor",
#   "peso": "un valor",
#   "velocidad": "un valor",
#   "tecnologiaPredominante": "un valor",
#   "rangoVoltaje": "un valor",
#   "rangoPresion": "un valor",
#   "rangoHumedad": "un valor",
#   "rangoCorriente": "un valor",
#   "rangoFrecuencia": "un valor",
#   "diagnostico": "un valor",
#   "rehabilitacion": "un valor",
#   "prevencion": "un valor",
#   "tratamientoVida": "un valor",
#   "analisisLaboratorio": "un valor",
#   "clasificacion": "un valor",
#   "periodicidad": "un valor",
#   "calibracion": "un valor"}
if __name__ == "__main__":
    uvicorn.run(app)
