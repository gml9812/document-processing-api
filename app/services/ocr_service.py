from google.cloud import vision
import io

async def extract_text_from_image(file):
    # Initialize Google Cloud Vision client
    client = vision.ImageAnnotatorClient()

    # Read the file content
    content = await file.read()
    image = vision.Image(content=content)

    # Perform OCR
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    
    return "" 