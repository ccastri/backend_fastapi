import json
from fastapi.testclient import TestClient
from main import app
import pytest

# Create a TestClient instance to simulate making requests
client = TestClient(app)


def test_hello_endpoint():
    response = client.get("/api/hola")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


if __name__ == "__main__":
    pytest.main()
