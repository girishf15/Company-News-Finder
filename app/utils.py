import os
import json

from app.config import DATA_DIR

def get_job_dir(job_id):
    return os.path.join(DATA_DIR, job_id)

def get_request_path(job_id):
    return os.path.join(get_job_dir(job_id), "request.json")

def get_results_path(job_id):
    return os.path.join(get_job_dir(job_id), "result.json")

def get_candidates_path(job_id):
    return os.path.join(get_job_dir(job_id), "candidates.jsonl")

def get_filtered_path(job_id):
    return os.path.join(get_job_dir(job_id), "filtered.jsonl")

def update_job_status(job_id, status):
    request_path = get_request_path(job_id)
    with open(request_path, "r") as f:
        request_data = json.load(f)
    request_data["status"] = status

    with open(request_path, "w") as f:
        json.dump(request_data, f)