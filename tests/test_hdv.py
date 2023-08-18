import json
import os
from fastapi.testclient import TestClient
from hoja_de_vida.hdv import timeout_dependency
from main import app  # Import your FastAPI app instance
from fastapi import HTTPException
from tempfile import NamedTemporaryFile

# Create a TestClient instance to simulate making requests
client = TestClient(app)

# Define test data for the request payload and image upload
test_data = {
    "departamento": "Test Departamento",
    "municipio": "Test Municipio",
    "entidad": "Test Entidad",
    "correo": "test@example.com",
    "direccion": "Test Address",
    "telefono": "123456789",
}

# Define the path to the test image
script_directory = os.path.dirname(__file__)
img_path = os.path.join(script_directory, "../uploaded_images/IMG_20190611_052353.jpg")


# Define a test timeout dependency
async def mock_timeout_dependency(seconds: int = 10):
    yield


app.dependency_overrides[timeout_dependency] = mock_timeout_dependency


# Test the fill_excel endpoint
# Test the fill_excel endpoint
def test_fill_excel_endpoint():
    # Use a named temporary file to hold the image data
    with NamedTemporaryFile(suffix=".jpg") as img_temp_file:
        with open(img_path, "rb") as img_file:
            img_temp_file.write(img_file.read())
            img_temp_file.seek(0)

            # Create the request payload with JSON data and the image
            request_payload = {
                "data": json.dumps(test_data),
            }

            # Perform the POST request
            response = client.post(
                "/api/hdv/fill_excel",
                data=request_payload,
                files={"img": ("test_image.jpg", img_temp_file, "image/jpeg")},
            )

            print("Response Status Code:", response.status_code)
            print("Response Headers:", response.headers)
            # print("Response Content:", response.content)

            if response.status_code == 400:
                assert response.json()["detail"] == "Error serializando el JSON."
            elif response.status_code == 500:
                assert response.json()["detail"] == "Ocurrió un error en el servidor."
            elif response.status_code == 503:
                assert response.json()["detail"] == "Request timed out"
            elif response.status_code == 422:
                assert response.json()["detail"][0]["msg"] == "str type expected"
            else:
                assert response.status_code == 200
                assert (
                    response.headers["content-type"]
                    == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            # Optionally, you can also assert specific details in the log if you're logging them
            # For example, to assert that certain log messages were generated:
            # assert "Error al procesar los datos" in captured_log_messages
            # assert "Error al abrir el archivo de plantilla" in captured_log_messages
