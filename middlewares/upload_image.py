from fastapi import FastAPI, File, UploadFile, APIRouter, HTTPException
import os
from pydantic import BaseModel

router = APIRouter(prefix="/middleware", tags=["upload"])


@router.post("/upload_image")
async def upload_image(img: UploadFile = File(...)):
    try:
        # Create the "uploaded_images" directory if it doesn't exist
        if not os.path.exists("uploaded_images"):
            os.makedirs("uploaded_images")

        # Save the uploaded image to the local directory
        image_path = os.path.join("uploaded_images", img.filename)
        with open(image_path, "wb") as img_file:
            img_file.write(img.file.read())

        return {"message": "Image uploaded successfully", "image_path": image_path}
    except FileNotFoundError as file_error:
        error_message = f"Error al abrir el archivo de plantilla: {str(file_error)}"
        logging.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)
    except Exception as e:
        # Handle other exceptions and provide a generic error message
        error_message = f"Error al procesar los datos: {str(e)}"
        logging.error(error_message)
        raise HTTPException(status_code=500, detail="Ocurrió un error en el servidor.")
