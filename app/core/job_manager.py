"""
Bellek-içi basit iş yöneticisi (queued → running → finished/failed).
"""

import asyncio
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Optional

# ────────────────────────────────────────────────────────────────────────────────
# Veri modeli & depolama
# ────────────────────────────────────────────────────────────────────────────────


@dataclass
class Job:
    id: str
    status: str = "queued"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


_jobs: Dict[str, Job] = {}


def create_job() -> Job:
    job = Job(id=str(uuid.uuid4()))
    _jobs[job.id] = job
    return job


def get_job(job_id: str) -> Optional[Job]:
    return _jobs.get(job_id)


# ────────────────────────────────────────────────────────────────────────────────
# Çalıştırıcı
# ────────────────────────────────────────────────────────────────────────────────


async def _run_job(job: Job, coro) -> None:  # pragma: no cover
    job.status = "running"
    try:
        job.result = await coro
        job.status = "finished"
    except Exception as exc:  # pragma: no cover
        job.error = str(exc)
        job.status = "failed"


def _run_job_sync(job: Job, coro) -> None:
    """ThreadPool içinden çağrılır → kendi event-loop’unu yönetir."""
    asyncio.run(_run_job(job, coro))


def schedule(coro, background_tasks) -> Job:
    """
    • Yeni Job kaydı oluşturur  
    • FastAPI BackgroundTasks’e job’u senkron fonksiyon olarak ekler
    • HTTP yanıtında job_id döner
    """
    job = create_job()
    background_tasks.add_task(_run_job_sync, job, coro)
    return job
