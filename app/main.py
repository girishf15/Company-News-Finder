import os
import uuid
import json
import asyncio
import datetime

from fastapi import FastAPI

from app.models import JobRequest
from app.config import DATA_DIR, FIXTURES_DIR, BASE_DIR, STATUS_PROCESSING

from app.job_processor import process_job
from app.utils import *

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/jobs/{job_id}/status")
def get_job_status(job_id):
    status_path = get_request_path(job_id)
    if os.path.exists(status_path):
        with open(status_path, "r") as f:
            request_data = json.load(f)
        return {"job_id": job_id, "status": request_data.get("status", "Unknown")}
    else:
        return {"job_id": job_id, "status": "Not Found"}


@app.get("/api/jobs/{job_id}/results")
def get_job_results(job_id):
    results_path = get_results_path(job_id)
    if os.path.exists(results_path):
        with open(results_path, "r") as f:
            results = json.load(f)
        return {"job_id": job_id, "results": results}
    else:
        return {"job_id": job_id, "results": None}

@app.get("/metrics")
def get_metrics():
    total_jobs = 0
    successful_jobs = 0
    failed_jobs = 0
    processing_jobs = 0

    # Iterate through directories in DATA_DIR
    import glob

    dirs = [path for path in glob.glob(f"{DATA_DIR}/*") if os.path.isdir(path)]
    for dir_path in dirs:
        request_file = os.path.join(dir_path, "request.json")
        # Read and parse request.json
        with open(request_file, "r") as f:
            request_data = json.load(f)
            status = request_data.get("status", "Unknown")
            print(f"Job ID: {request_data.get('job_id')} Status: {status}")
            total_jobs += 1

            # Update metrics based on status
            if status == "Completed":
                successful_jobs += 1
            elif status == "Failed":
                failed_jobs += 1
            elif status == "Processing":
                processing_jobs += 1

    # Return metrics
    metrics = {
        "total_jobs": total_jobs,
        "successful_jobs": successful_jobs,
        "failed_jobs": failed_jobs,
        "processing_jobs": processing_jobs,
    }
    return metrics

@app.post("/api/jobs/start")
async def start_job(request: JobRequest):

    job_id = str(uuid.uuid4())
    job_dir = get_job_dir(job_id)
    os.makedirs(job_dir, exist_ok=True)

    request_data = {
        "job_id": job_id,
        "company_name": request.company_name,
        "address": request.address,
        "months": request.months,   
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": STATUS_PROCESSING,
    }

    with open(get_request_path(job_id), "w") as f:
        json.dump(request_data, f, indent=4)

    asyncio.create_task(process_job(job_id, request.company_name, request.months))

    return {"job_id": job_id, "message": "Job started"}
