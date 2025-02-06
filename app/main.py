from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import logging
from app.core.processor_factory import DocumentProcessorFactory
from app.core.llm_provider_factory import get_llm_provider
from app.config import get_settings
from app.services.ocr_service import extract_text_from_image

import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("document-processing-api")

app = FastAPI()

@app.post("/{document_type}")
async def process_document(
    document_type: str,
    keywords: str = Form(...),
    document_file: UploadFile = File(...),
    language: str = Form(...),
    llm_provider: str = Form(default="gemini"),
    model_name: str = Form(default="gemini-1.5-flash")
):
    try:
        settings = get_settings()
        
        logger.info(f"New OCR request received for document type: {document_type}")
        # Create LLM provider
        llm = get_llm_provider(llm_provider, settings)
        logger.info(f"LLM provider '{llm_provider}' successfully obtained.")
        
        # Get document processor
        processor = DocumentProcessorFactory.get_processor(
            document_type=document_type,
            llm_provider=llm,
            model_name=model_name
        )
        
        # Extract text using OCR
        extracted_text = await extract_text_from_image(document_file)
        logger.info("Text successfully extracted using OCR.")
        logger.info(f"Extracted text: {extracted_text}")
        
        # Process document
        keyword_list = [k.strip() for k in keywords.split(',')]
        result = await processor.process_document(extracted_text, keyword_list, language)
        logger.info("Document successfully processed.")
        
        return result
    except ValueError as e:
        logger.error(f"Error processing document: {e}")
        raise HTTPException(status_code=422, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 