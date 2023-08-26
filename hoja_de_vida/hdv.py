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

#! JSON serialization error handling
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError

#! Excel template manipulation
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

#! Binary (file) response config
from fastapi.responses import FileResponse
from datetime import date, datetime

#! General error handling
import logging
import os

#! Temporary files/ directories
import tempfile
from typing import List
import json
from async_timeout import timeout
import asyncio
import time
from PIL import Image as PILImage

#! Router config
router = APIRouter(prefix="/hdv", tags=["add"])


#! Pydantic JSON serialization (to python dict) modell
class Data(BaseModel):
    departamento: str
    municipio: str
    entidad: str
    correo: str
    direccion: str
    telefono: str


# !Rest of hdv fields
# equipo: str
# marca: str
# modelo: str
# serie: str
# activoFijo: str
# registroSanitario: str
# ubicacion: str
# proveedor: str
# AdquisitionWay: str
# yearOfFabrication: date
# boughtDate: date
# installationDate: date
# warrantyEnd: date
# fabricante: str
# tension: str
# potencia: str
# presion: str
# corriente: str
# frecuencia: str
# rangoTemperatura: str
# peso: str
# velocidad: str
# tecnologiaPredominante: str
# rangoVoltaje: str
# rangoPresion: str
# rangoHumedad: str
# rangoCorriente: str
# rangoFrecuencia: str
# diagnostico: str
# rehabilitacion: str
# prevencion: str
# tratamientoVida: str
# analisisLaboratorio: str
# filteredInputs: List[str] = Field(default_factory=list)
# clasificacion: str = None
# periodicidad: str = None
# calibracion: str = None
# copiaRegistroSanitario: str = None
# copiaRegistroImportacion: str = None
# copiaFactura: str = None
# copiaIngresoAlmacen: str = None
# copiaActaReciboSatisfaccion: str = None
# Maximum allowed image size in bytes
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# Allowed image MIME types
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}


def is_allowed_image_type(content_type):
    return content_type in ALLOWED_IMAGE_TYPES


def is_valid_image(image_path):
    try:
        with PILImage.open(image_path) as img:
            img.verify()
            return True
    except Exception as e:
        return False


#! Dependency for handling when request
#! runs out of time (10 seconds)
async def timeout_dependency(seconds: int = 10):
    async with timeout(seconds) as time_limit:
        yield
    if time_limit.expired:
        raise HTTPException(status_code=503, detail="Request timed out")


@router.post(
    "/fill_excel",
)
async def fill_excel(
    data: str = File(...),
    img: UploadFile = File(...),
    timeout_dep: None = Depends(timeout_dependency),
):
    try:
        #! Start response timer
        start_time = time.time()
        #! from JSON.stringify to JSON
        json_data = json.loads(data)
        # try:
        #! instanciating a new Data pydantic model with JSON props
        form_data_instance = Data(**json_data)
        # except ValidationError as validation_error:
        # raise HTTPException(status_code=400, detail=validation_error.errors())
        #! instanciating a new Data pydantic model with JSON props
        # form_data_instance = Data(**json_data)
        #! from JSON to Python dictionary
        form_data_dict = form_data_instance.dict()

        # Start counting how long takes the api to
        # send back the response
        #! Assinging dictionary keys to  variables
        departamento = form_data_dict["departamento"]
        municipio = form_data_dict["municipio"]
        entidad = form_data_dict["entidad"]
        correo = form_data_dict["correo"]
        direccion = form_data_dict["direccion"]
        telefono = form_data_dict["telefono"]
        # print(telefono)
        # print(data.img)
        #! Creating a temp file:
        #!1. Store current file path
        module_directory = os.path.dirname(__file__)
        #!2. Name the temporal file and add it to the current directory path
        excel_template_path = os.path.join(module_directory, "hdv_template.xlsx")
        #!3. Cargar el archivo Excel hoja_De_vida.xlsx
        workbook = load_workbook(excel_template_path)
        sheet = workbook.active

        #!4 Llenar los campos del archivo Excel con los datos recibidos tipo AllFormData
        # provenientes de Next JS:
        #! IV. I. Ubicacion geográfica
        sheet["C6"] = departamento
        sheet["C7"] = municipio
        sheet["C8"] = entidad
        sheet["C9"] = correo
        sheet["C10"] = direccion
        sheet["C11"] = telefono
        # sheet["C13"] = form_data_dict["equipo"]
        # sheet["C14"] = form_data_dict["marca"]
        # sheet["C15"] = form_data_dict["modelo"]
        # sheet["C16"] = form_data_dict["serie"]
        # sheet["C17"] = form_data_dict["activoFijo"]
        # sheet["C18"] = form_data_dict["registroSanitario"]
        # sheet["C19"] = form_data_dict["ubicacion"]
        # sheet["C20"] = form_data_dict["proveedor"]
        # Check image type
        if not is_allowed_image_type(img.content_type):
            raise HTTPException(status_code=400, detail="Invalid image type")

        # Check image size
        if img.file.seek(0, os.SEEK_END) > MAX_IMAGE_SIZE:
            raise HTTPException(status_code=400, detail="Image size exceeds the limit")

        #! Image processing:
        #! create a temporal directory
        temp_dir = tempfile.mkdtemp()

        #! Generate a temporary file path using the filename prop
        #! to be stored in the temp_dir in binary format
        temp_image_path = os.path.join(temp_dir, img.filename)
        # ! Open the img.bin
        with open(temp_image_path, "wb") as img_file:
            #! img writting by reading the incoming binaries
            img_file.write(img.file.read())
        # Check image validity
        if not is_valid_image(img):
            raise HTTPException(status_code=400, detail="Invalid image format")

        #! Open and resize the image using PILLOW
        pil_image = PILImage.open(temp_image_path)
        pil_image.thumbnail((800, 800))  # Resize the image
        #! Save the compressed image back to the temporary path
        compressed_image_path = os.path.join(temp_dir, "compressed_image.jpg")
        #! Downsampling .85 in JPEG format
        pil_image.save(
            compressed_image_path, format="JPEG", quality=85
        )  # Adjust quality as needed

        #! Add the compressed image to the Excel
        #! Using openpyxl
        img = Image(compressed_image_path)
        img.width = 250  # Set the width of the image
        img.height = 155  # Set the height of the image
        img_anchor = "H5"  # The top-left cell for the image
        sheet.add_image(img, img_anchor)

        # sheet["G13"] = form_data_dict["AdquisitionWay"]
        # form_data_dict["yearOfFabrication"] = datetime.strptime(
        # form_data_dict["yearOfFabrication"], "%Y-%m-%d"
        # )
        # form_data_dict["boughtDate"] = datetime.strptime(
        #     form_data_dict["boughtDate"], "%Y-%m-%d"
        # )
        # form_data_dict["installationDate"] = datetime.strptime(
        #     form_data_dict["installationDate"], "%Y-%m-%d"
        # )
        # form_data_dict["warrantyEnd"] = datetime.strptime(
        #     form_data_dict["warrantyEnd"], "%Y-%m-%d"
        # )
        # # Extract year, month, and day
        # year = form_data_dict["yearOfFabrication"].year
        # month = form_data_dict["yearOfFabrication"].month
        # day = form_data_dict["yearOfFabrication"].day
        # sheet["H16"] = day
        # sheet["I16"] = month
        # sheet["J16"] = year
        # year_boughtDate = form_data_dict["boughtDate"].year
        # month_boughtDate = form_data_dict["boughtDate"].month
        # day_boughtDate = form_data_dict["boughtDate"].day
        # sheet["H17"] = day_boughtDate
        # sheet["I17"] = month_boughtDate
        # sheet["J17"] = year_boughtDate
        # year_installationDate = form_data_dict["installationDate"].year
        # month_installationDate = form_data_dict["installationDate"].month
        # day_installationDate = form_data_dict["installationDate"].day
        # sheet["H18"] = day_installationDate
        # sheet["I18"] = month_installationDate
        # sheet["J18"] = year_installationDate
        # year_warrantyEnd = form_data_dict["warrantyEnd"].year
        # month_warrantyEnd = form_data_dict["warrantyEnd"].month
        # day_warrantyEnd = form_data_dict["warrantyEnd"].day
        # sheet["H19"] = day_warrantyEnd
        # sheet["I19"] = month_warrantyEnd
        # sheet["J19"] = year_warrantyEnd

        # # # sheet["G17"] = form_data_dictform_data_dictform_data_dict.warrantyEnd
        # # sheet["F20"] = form_data_dictform_data_dict.fabricante

        # sheet["C23"] = form_data_dict["tension"]
        # sheet["C24"] = form_data_dict["potencia"]
        # sheet["C25"] = form_data_dict["presion"]
        # sheet["G23"] = form_data_dict["corriente"]
        # sheet["G24"] = form_data_dict["frecuencia"]
        # sheet["G25"] = form_data_dict["rangoTemperatura"]
        # sheet["J23"] = form_data_dict["peso"]
        # sheet["J24"] = form_data_dict["velocidad"]
        # sheet["J25"] = form_data_dict["tecnologiaPredominante"]

        # sheet["C27"] = form_data_dict["rangoVoltaje"]
        # sheet["C28"] = form_data_dict["rangoPresion"]
        # sheet["C29"] = form_data_dict["rangoHumedad"]
        # sheet["C30"] = form_data_dict["rangoCorriente"]
        # sheet["C31"] = form_data_dict["rangoFrecuencia"]

        # sheet["H27"] = form_data_dict["diagnostico"]
        # sheet["H28"] = form_data_dict["rehabilitacion"]
        # sheet["H29"] = form_data_dict["prevencion"]
        # sheet["H30"] = form_data_dict["tratamientoVida"]
        # sheet["H31"] = form_data_dict["analisisLaboratorio"]

        # sheet["A34"] = form_data_dict["clasificacion"]
        # sheet["E34"] = form_data_dict["periodicidad"]
        # sheet["H34"] = form_data_dict["calibracion"]
        # #   Define the starting row for columns A and E
        # start_row_A = 36
        # start_row_E = 36
        # # print(form_data_dict['filteredInputs'])
        # filtered_inputs = form_data_dict.get("filteredInputs", [])
        # # Loop through the filteredInputs list and assign them to cells in the specified pattern
        # for idx, input_value in enumerate(filtered_inputs):
        #     if idx < 3:
        #         cell_row_A = start_row_A + idx
        #         cell = sheet[f"A{cell_row_A}"]
        #         cell.value = input_value
        #     elif idx < 6:
        #         cell_row_E = start_row_E + (idx - 3)
        #         cell = sheet[f"E{cell_row_E}"]
        #         cell.value = input_value

        # field_value_mappings = {
        #     "copiaRegistroSanitario": form_data_dict.copiaRegistroSanitario,
        #     "copiaRegistroImportacion": form_data_dict.copiaRegistroImportacion,
        #     "copiaFactura": form_data_dict.copiaFactura,
        #     "copiaIngresoAlmacen": form_data_dict.copiaIngresoAlmacen,
        #     "copiaActaReciboSatisfaccion": form_data_dict.copiaActaReciboSatisfaccion,
        #     # Add other fields and values here
        # }
        # start_row = 53
        # end_row = 64
        # columns = ["H", "I", "J", "K", "L", "M"]

        # for field_name, field_value in field_value_mappings.items():
        #     if hasattr(data, field_name):
        #         for row_idx in range(start_row, end_row + 1):
        #             for col_letter in columns:
        #                 cell_value = sheet[f"{col_letter}{row_idx}"].value
        #                 if cell_value == field_value:
        #                     sheet[f"{col_letter}{row_idx}"] = "X"
        # Llenar los otros campos del formulario
        # II. ...
        #! Guardar el archivo Excel modificado en un directorio temporal
        temp_excel_file_path = os.path.join(module_directory, "hdv_temp.xlsx")
        workbook.save(temp_excel_file_path)
        #!ending the response timer
        end_time = time.time()
        #! calculate total response time
        processing_time = end_time - start_time
        print(processing_time)
        #!Response as a binary file with the xlsx format
        return FileResponse(
            temp_excel_file_path,
            filename="hdv_template.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=myfile.xlsx"},
        )

    except json.JSONDecodeError as json_error:
        print("JSON Decoding Error:", json_error)
        raise HTTPException(status_code=400, detail="Error serializando el JSON.")
    except FileNotFoundError as file_error:
        error_message = f"Error al abrir el archivo de plantilla: {str(file_error)}"
        logging.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)
    except ValueError as value_error:
        error_message = f"Error en los valores de entrada: {str(value_error)}"
        logging.error(error_message)
        raise HTTPException(status_code=400, detail=error_message)
    except PermissionError as permission_error:
        error_message = f"Error de permisos: {str(permission_error)}"
        logging.error(error_message)
        raise HTTPException(status_code=403, detail=error_message)
    except IOError as io_error:
        error_message = f"Error de entrada/salida: {str(io_error)}"
        logging.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)
    except Exception as e:
        # Handle other exceptions and provide a generic error message
        error_message = f"Error al procesar los datos: {str(e)}"
        logging.error(error_message)
        raise HTTPException(status_code=500, detail="Ocurrió un error en el servidor.")
