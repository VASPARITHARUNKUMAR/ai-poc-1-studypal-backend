from fastapi import APIRouter, UploadFile, Form
from services.ingestion import ingest_and_embed

router = APIRouter()

@router.post("/upload/")
async def upload_files(
    semester: str = Form(...),
    subject: str = Form(...),
    files: list[UploadFile] = ...
):
    results = await ingest_and_embed(semester, subject, files)
    return {"status": "success", "details": results}
