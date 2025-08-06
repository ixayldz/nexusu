from fastapi import APIRouter, BackgroundTasks

from app.agents.planner import PlanRequest, PlannerAgent
from app.agents.builder import BuildRequest, BuilderAgent
from app.agents.tester import TestRequest, TesterAgent
from app.core.job_manager import schedule

router = APIRouter(prefix="/tasks", tags=["tasks"])

planner = PlannerAgent()
builder = BuilderAgent()
tester = TesterAgent()


@router.post("/plan")
async def plan_task(req: PlanRequest):
    """LLM tabanlı plan (şimdilik mock)."""
    return await planner.run(req)


@router.post("/build")
async def build_task(req: BuildRequest, background_tasks: BackgroundTasks):
    """Plan adımlarını arka planda derleyip job_id döner."""
    job = schedule(builder.run(req), background_tasks)
    return {"job_id": job.id, "status": job.status}


@router.post("/test")
async def test_task(req: TestRequest, background_tasks: BackgroundTasks):
    """Artifact’ları arka planda test eder, job_id döner."""
    job = schedule(tester.run(req), background_tasks)
    return {"job_id": job.id, "status": job.status}
