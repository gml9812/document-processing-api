from typing import Dict, Type
from .document_processor import DocumentProcessor
from .llm_provider import LLMProvider
from app.processors.business_license_processor import BusinessLicenseProcessor
from app.processors.invoice_processor import InvoiceProcessor

class DocumentProcessorFactory:
    _processors: Dict[str, Type[DocumentProcessor]] = {
        "business_license": BusinessLicenseProcessor,
        "invoice": InvoiceProcessor
    }
    
    @classmethod
    def get_processor(cls, document_type: str, llm_provider: LLMProvider, model_name: str) -> DocumentProcessor:
        processor_class = cls._processors.get(document_type)
        if not processor_class:
            raise ValueError(f"Unsupported document type: {document_type}")
        return processor_class(llm_provider=llm_provider, model_name=model_name) 