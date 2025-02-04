from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from app.core.processor_factory import DocumentProcessorFactory
from app.core.llm_provider_factory import get_llm_provider
from app.config import get_settings
from app.services.ocr_service import extract_text_from_image

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
        
        # Create LLM provider
        llm = get_llm_provider(llm_provider, settings)
        
        # Get document processor
        processor = DocumentProcessorFactory.get_processor(
            document_type=document_type,
            llm_provider=llm,
            model_name=model_name
        )
        
        # Extract text using OCR
        extracted_text = await extract_text_from_image(document_file)
        
        # Process document
        keyword_list = [k.strip() for k in keywords.split(',')]
        result = await processor.process_document(extracted_text, keyword_list, language)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 