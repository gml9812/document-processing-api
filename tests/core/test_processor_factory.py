import pytest
from app.core.processor_factory import DocumentProcessorFactory
from app.processors.business_license_processor import BusinessLicenseProcessor
from app.processors.invoice_processor import InvoiceProcessor

def test_get_processor_business_license():
    factory = DocumentProcessorFactory()
    processor = factory.get_processor("business_license", "test_api_key")
    assert isinstance(processor, BusinessLicenseProcessor)

def test_get_processor_invoice():
    factory = DocumentProcessorFactory()
    processor = factory.get_processor("invoice", "test_api_key")
    assert isinstance(processor, InvoiceProcessor)

def test_get_processor_unsupported_type():
    factory = DocumentProcessorFactory()
    with pytest.raises(ValueError) as excinfo:
        factory.get_processor("unknown_type", "test_api_key")
    assert "Unsupported document type" in str(excinfo.value)