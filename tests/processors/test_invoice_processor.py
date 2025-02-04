import pytest
from unittest.mock import AsyncMock
from app.processors.invoice_processor import InvoiceProcessor
from app.schemas.invoice import Invoice
from app.core.llm_provider import LLMMessage, LLMConfig

@pytest.fixture
def mock_llm():
    mock = AsyncMock()
    mock.generate.return_value = "cleaned text"
    mock.generate_with_json_output.return_value = {
        "invoice_number": "INV-001",
        "company_name": "Test Company"
    }
    return mock

@pytest.fixture
def invoice_processor(mock_llm):
    processor = InvoiceProcessor(api_key="test_key")
    processor.llm = mock_llm
    return processor

@pytest.mark.asyncio
async def test_process_document_successful_extraction(invoice_processor, mock_llm):
    text = "raw invoice text"
    keywords = ["invoice number", "company name"]
    language = "en"
    
    result = await invoice_processor.process_document(text, keywords, language)
    
    assert isinstance(result, Invoice)
    assert result.invoice_number == "INV-001"
    assert result.company_name == "Test Company"
    
    mock_llm.generate.assert_called_once()
    mock_llm.generate_with_json_output.assert_called_once() 