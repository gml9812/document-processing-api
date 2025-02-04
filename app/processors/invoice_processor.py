from app.core.document_processor import DocumentProcessor
from app.schemas.invoice import Invoice
from app.core.llm_provider import LLMMessage
from typing import List

class InvoiceProcessor(DocumentProcessor[Invoice]):
    async def process_document(self, text: str, keywords: List[str], language: str) -> Invoice:
        # Step 1: Clean text
        cleanup_messages = [
            LLMMessage(
                role="system",
                content="Clean and organize raw OCR text from invoices. Focus on invoice number, company details, dates, and itemized list of charges."
            ),
            LLMMessage(
                role="user",
                content=f"Clean this text:\n{text}"
            )
        ]
        cleaned_text = await self._generate_response(cleanup_messages)

        # Step 2: Extract information
        schema = Invoice.model_json_schema()
        extraction_messages = [
            LLMMessage(
                role="system",
                content="Extract invoice information focusing on: " + ", ".join(keywords)
            ),
            LLMMessage(
                role="user",
                content=f"Extract information from:\n{cleaned_text}"
            )
        ]
        
        extracted_data = await self._generate_structured_response(
            extraction_messages,
            schema
        )
        
        return Invoice(**extracted_data) 