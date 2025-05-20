import os
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.tasks import process_prospect

router = APIRouter(prefix="/prospect", tags=["Prospect"])
BASE_DIR = os.getcwd()
STORAGE_DIR = os.path.join(BASE_DIR, "data", "prospects")
os.makedirs(STORAGE_DIR, exist_ok=True)

@router.post("/upload")
async def upload_prospect(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in {".pdf", ".docx", ".doc"}:
        raise HTTPException(status_code=400, detail="Formato no soportado")
    job_id = str(uuid4())
    filename = f"{job_id}{ext}"
    dest_path = os.path.join(STORAGE_DIR, filename)
    with open(dest_path, "wb") as f:
        f.write(await file.read())

    task = process_prospect.delay(job_id, filename)
    return {"job_id": job_id, "task_id": task.id}
