import os
import uuid
import json
import asyncio
import datetime

from fastapi import FastAPI

from app.models import JobRequest
from app.config import DATA_DIR, FIXTURES_DIR, BASE_DIR

from app.job_processor import process_job

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/jobs/{job_id}/status")
def get_job_status(job_id):
    return {"job_id": job_id, "status": "processing"}

@app.get("/api/jobs/{job_id}/results")
def get_job_results(job_id):
    return {"job_id": job_id, "results": []}

@app.get("/metrics")
def get_metrics():
    return {"metrics": {
        "total_jobs": 10,
        "successful_jobs": 8,
        "failed_jobs": 2,
    }}

@app.post("/api/jobs/start")
async def start_job(request: JobRequest):

    job_id = str(uuid.uuid4())
    job_dir = os.path.join(DATA_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    request_data = {
        "job_id": job_id,
        "company_name": request.company_name,
        "address": request.address,
        "months": request.months,   
        "timestamp": datetime.now(datetime.timezone.utc).isoformat()
    }

    with open(os.path.join(job_dir, "request.json"), "w") as f:
        json.dump(request_data, f, indent=4)

    asyncio.create_task(process_job(job_id, request.company_name))

    return {"job_id": job_id, "message": "Job started"}
