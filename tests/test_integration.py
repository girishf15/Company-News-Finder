import os
import json
import time
from fastapi.testclient import TestClient
from app.config import STATUS_COMPLETED, STATUS_PROCESSING
from app.main import app
from app.utils import get_job_dir, get_request_path

client = TestClient(app)

def test_job_processing():

    company_name = "Tesla Inc"
    address = "Mumbai, India"
    months = 1
    
    response = client.post(
        "/api/jobs/start",
        json={"company_name": company_name, "address": address, "months": months}
    )
    
    assert response.status_code == 200
    assert response.json().get("status") == STATUS_PROCESSING

    job_id = response.json()["job_id"]
    
    time.sleep(5)

    job_dir = get_job_dir(job_id)
    request_path = get_request_path(job_id)
    
    assert os.path.exists(job_dir) == True
    assert os.path.exists(request_path) == True
    
    with open(request_path, "r") as f:
        request_data = json.load(f)
    
    assert request_data["company_name"] == company_name
    assert request_data["job_id"] == job_id
    assert request_data["status"] == STATUS_COMPLETED