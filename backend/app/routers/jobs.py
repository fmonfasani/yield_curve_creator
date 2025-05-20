import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse

router = APIRouter(prefix="/jobs", tags=["Jobs"])
BASE_DIR = os.getcwd()
RESULTS_DIR = os.path.join(BASE_DIR, "data", "results")

@router.get("/{job_id}")
async def get_job(job_id: str):
    result_path = os.path.join(RESULTS_DIR, f"{job_id}.json")
    if not os.path.exists(result_path):
        return JSONResponse(status_code=200, content={"status": "processing"})
    try:
        return FileResponse(path=result_path, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al devolver resultado: {e}")
