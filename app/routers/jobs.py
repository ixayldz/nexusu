from fastapi import APIRouter, HTTPException

from app.core.job_manager import get_job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}")
async def job_status(job_id: str):
    """
    Job’ın anlık durumunu (queued/running/finished/failed) ve sonucunu döner.
    """
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "id": job.id,
        "status": job.status,
        "result": job.result,
        "error": job.error,
    }
