from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import uuid
from datetime import datetime
import fitz
from docx import Document
import tempfile
import os

app = FastAPI()


class GeminiResult(BaseModel):
    classification: str
    sentiment: str
    confidence_score: float
    entities: dict


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/categories")
def categories():
    return {
        "categories": [
            "invoice",
            "contract",
            "purchase_order",
            "vendor_agreement",
            "other"
        ]
    }


@app.post("/sensitivity")
def sensitivity(data: dict):
    text = str(data)

    if any(word in text.lower() for word in ["salary", "ssn", "credit card"]):
        return {"sensitivity": "confidential"}

    return {"sensitivity": "internal"}


@app.post("/enrich")
def enrich(data: GeminiResult):

    department_map = {
        "invoice": "Finance",
        "contract": "Legal",
        "purchase_order": "Procurement",
        "vendor_agreement": "Vendor Management",
        "other": "General"
    }

    department = department_map.get(
        data.classification,
        "General"
    )

    routing_tag = (
        "needs-review"
        if data.confidence_score < 0.7
        else "auto-approved"
    )

    return {
        "document_id": str(uuid.uuid4()),
        "department": department,
        "routing_tag": routing_tag,
        "processed_at": datetime.utcnow().isoformat(),
        "sensitivity": "internal"
    }


@app.post("/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name

    text = ""

    try:
        pdf = fitz.open(temp_path)

        for page in pdf:
            text += page.get_text()

        pdf.close()

        return {
            "filename": file.filename,
            "extracted_text": text
        }

    finally:
        os.remove(temp_path)


@app.post("/extract-docx")
async def extract_docx(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name

    try:
        doc = Document(temp_path)

        text = "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )

        return {
            "filename": file.filename,
            "extracted_text": text
        }
    

    finally:
        os.remove(temp_path)
    
@app.post("/extract-txt")
async def extract_txt(file: UploadFile = File(...)):

    content = await file.read()

    try:
           text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = content.decode("latin-1")

    return {
        "filename": file.filename,
           "extracted_text": text
        }