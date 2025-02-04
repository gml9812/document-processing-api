import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.mark.asyncio
async def test_process_business_license_api(test_client):
    mock_processor = AsyncMock()
    mock_processor.process_document.return_value = {"business_name": "Test Business"}
    mock_ocr_service = AsyncMock(return_value="extracted text from OCR")

    with patch("app.core.processor_factory.DocumentProcessorFactory.get_processor", return_value=mock_processor):
        with patch("app.services.ocr_service.extract_text_from_image", mock_ocr_service):
            with open("tests/test_image.png", "rb") as f:
                files = {"document_file": ("test_image.png", f, "image/png")}
                data = {"keywords": "business name", "language": "en"}
                response = test_client.post("/business_license", files=files, data=data)
                assert response.status_code == 200
                assert response.json() == {"business_name": "Test Business"}
                mock_processor.process_document.assert_called_once_with("extracted text from OCR", ['business name'], 'en')