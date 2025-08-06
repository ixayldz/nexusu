from fastapi import APIRouter, BackgroundTasks

from app.agents.planner import PlanRequest, PlannerAgent, PlanResponse
from app.agents.builder import BuildRequest, BuilderAgent, BuildResponse
from app.agents.tester import TestRequest, TesterAgent, TestResponse
from app.core.job_manager import schedule

router = APIRouter(prefix="/tasks", tags=["tasks"])

planner = PlannerAgent()
builder = BuilderAgent()
tester = TesterAgent()


@router.post("/plan", response_model=PlanResponse)
async def plan_task(req: PlanRequest):
    return await planner.run(req)


@router.post("/build", response_model=dict)
async def build_task(req: BuildRequest, background_tasks: BackgroundTasks):
    job = schedule(builder.run(req), background_tasks)
    return {"job_id": job.id, "status": job.status}


@router.post("/test", response_model=dict)
async def test_task(req: TestRequest, background_tasks: BackgroundTasks):
    job = schedule(tester.run(req), background_tasks)
    return {"job_id": job.id, "status": job.status}
