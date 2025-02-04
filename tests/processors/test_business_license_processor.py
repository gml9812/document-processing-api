import pytest
from unittest.mock import AsyncMock
from app.processors.business_license_processor import BusinessLicenseProcessor
from app.schemas.business_license import BusinessLicense
from app.core.llm_provider import LLMMessage, LLMConfig, LLMProvider

class MockLLMProvider(LLMProvider):
    def __init__(self):
        self.generate = AsyncMock()
        self.generate_with_json_output = AsyncMock()

@pytest.fixture
def mock_llm():
    provider = MockLLMProvider()
    provider.generate.return_value = "cleaned text"
    provider.generate_with_json_output.return_value = {
        "business_name": "Test Business"
    }
    return provider

@pytest.fixture
def business_license_processor(mock_llm):
    return BusinessLicenseProcessor(llm_provider=mock_llm, model_name="test-model")

@pytest.mark.asyncio
async def test_process_document_successful_extraction(business_license_processor, mock_llm):
    text = "raw license text"
    keywords = ["business name"]
    language = "en"
    
    mock_llm.generate.return_value = "No issues found"
    
    result = await business_license_processor.process_document(text, keywords, language)
    
    assert isinstance(result, BusinessLicense)
    assert result.business_name == "Test Business"
    
    assert mock_llm.generate.call_count == 2  # cleanup and validation
    mock_llm.generate_with_json_output.assert_called_once()  # extraction

@pytest.mark.asyncio
async def test_process_document_validation_failure(business_license_processor, mock_llm):
    mock_llm.generate.side_effect = ["cleaned text", "ISSUE: Registration number is invalid"]
    text = "raw license text"
    keywords = ["business name"]
    language = "en"
    
    with pytest.raises(ValueError) as excinfo:
        await business_license_processor.process_document(text, keywords, language)
    assert "Validation failed" in str(excinfo.value)