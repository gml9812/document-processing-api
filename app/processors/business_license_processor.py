from app.core.document_processor import DocumentProcessor
from app.schemas.business_license import BusinessLicense
from app.core.llm_provider import LLMMessage
from typing import List


import logging
logger = logging.getLogger("document-processing-api")

class BusinessLicenseProcessor(DocumentProcessor[BusinessLicense]):
    async def process_document(self, text: str, keywords: List[str], language: str) -> BusinessLicense:
        # Step 1: Clean text
        cleanup_messages = [
            LLMMessage(
                role="system",
                content="""You are a precise business license document analyzer. 
                Your task is to clean and organize raw OCR text from business licenses.
                Focus on business name, registration number, address, and issue date."""
            ),
            LLMMessage(
                role="user",
                content=f"Clean this text:\n{text}"
            )
        ]
        cleaned_text = await self._generate_response(cleanup_messages)

        logger.info(f"Cleaned text: {cleaned_text}")

        # Step 2: Extract information
        schema = BusinessLicense.model_json_schema()
        extraction_messages = [
            LLMMessage(
                role="system",
                content="""You are a business license information extractor.
                Extract ONLY information that you are completely certain about.
                Pay special attention to:
                - Business name
                - Registration number
                - Address
                - Issue date
                If you cannot find a specific field, mark it as null.
                DO NOT make assumptions or generate fake data."""
            ),
            LLMMessage(
                role="user",
                content=f"""Extract information from this text:
                {cleaned_text}
                
                Focus on these fields: {', '.join(keywords)}
                Language: {language}"""
            )
        ]
        
        extracted_data = await self._generate_structured_response(
            extraction_messages,
            schema
        )

        logger.info(f"Extracted data: {extracted_data}")
        
        # Step 3: Validate
        validation_messages = [
            LLMMessage(
                role="system",
                content="""You are a business license validation expert.
                Verify:
                1. Registration numbers are in the correct format
                2. Dates are valid and recent
                3. Business names and addresses are plausible
                Flag any inconsistencies or suspicious values."""
            ),
            LLMMessage(
                role="user",
                content=f"""Original text:
                {text}
                
                Extracted information:
                {extracted_data}
                
                Verify each field and identify any potential issues."""
            )
        ]
        validation_result = await self._generate_response(validation_messages)

        logger.info(f"Validation result: {validation_result}")
        
        if "ISSUE:" in validation_result:
            raise ValueError(f"Validation failed: {validation_result}")
        
        return BusinessLicense(**extracted_data)