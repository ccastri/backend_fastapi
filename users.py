from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from models.user_models_db import create_user
from models.user_models import UserRegister

router = APIRouter(prefix="/auth", tags=["create"])


# Route for filling out the excel template with the user's inputs
@router.post("/api/register", status_code=201)
async def create_user_route(user_data: UserRegister):
    try:
        new_user = create_user(user_data)
        return new_user
    except Exception as e:
        error_message = f"Error al procesar los datos: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)
