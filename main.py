from py_zerox.pyzerox import zerox
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import httpx
import time
import os

app = FastAPI()

@app.post("/api/pdf_extraction")
async def extract_pdf(pdf_file: UploadFile = File(...), document_id: str = Form(...)):
    # Save uploaded file
    temp_path = "./temp/uploaded.pdf"
    with open(temp_path, "wb") as buffer:
        content = await pdf_file.read()
        buffer.write(content)

    # Process with zerox
    zerox_result = await zerox(file_path=temp_path, temp_dir="./temp")

    # Build markdown
    markdown = ""
    for page in zerox_result.pages:
        markdown += page.content + "\n\n"

    patient_data = {}

    return JSONResponse({
        'markdown': markdown,
        'patientData': patient_data,
        'document_id': document_id
    })

# FastAPI Server
@app.post("/api/mock/pdf_extraction")
async def extract_pdf_mock(pdf_file: UploadFile = File(...), document_id: str = Form(...)):

    os.makedirs("./temp", exist_ok=True)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.join(base_dir, "temp")
    temp_path = os.path.join(temp_dir, "uploaded.pdf")
    print(temp_path)

    temp_path = "./temp/uploaded.pdf"
    with open(temp_path, "wb") as buffer:
        content = await pdf_file.read()
        buffer.write(content)

    time.sleep(1)  # Simulating processing time

    # Make a webhook call to your Next.js app
    webhook_url = "http://localhost:3000/api/documents/webhook/extraction"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            webhook_url,
            json={
                'document_id': document_id,
                'extraction_status': 'DONE',
                'extraction_text': "Mock text received from ML server",
            }
        )

    return JSONResponse({"status": "Processing completed"})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)