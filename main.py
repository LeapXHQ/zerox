from py_zerox.pyzerox import zerox
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/api/extract-pdf")
async def extract_pdf(pdf_file: UploadFile = File(...)):
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
        'patientData': patient_data
    })

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)