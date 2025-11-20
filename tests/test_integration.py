import os
import json
import time
from fastapi.testclient import TestClient
from app.config import STATUS_COMPLETED, STATUS_PROCESSING, FIXTURES_DIR
from app.main import app
from app.utils import get_job_dir, get_request_path, get_results_path

client = TestClient(app)

def test_job_processing():
    
    # Start job
    response = client.post(
        "/api/jobs/start",
        json={"company_name": "Tesla Inc", "address": "Mumbai, India", "months": 24}
    )
    
    assert response.status_code == 200
    job_id = response.json()["job_id"]
    
    # Wait for completion
    time.sleep(5)
    
    request_path = get_request_path(job_id)
    with open(request_path, "r") as f:
        request_data = json.load(f)
    assert request_data["status"] == STATUS_COMPLETED
    
    # verify with labels
    labels_path = os.path.join(FIXTURES_DIR, "labels.jsonl")
    with open(labels_path, "r") as f:
        for line in f:
            label = json.loads(line)
            if label["company"] == "Tesla Inc":
                expected_ids = set(label["relevant_article_ids"])
                break
    
    # Load actual results
    results_path = get_results_path(job_id)
    with open(results_path, "r") as f:
        results = json.load(f)
    
    predicted_ids = []
    for article in results["filtered_candidates"]:
        if article["id"] not in predicted_ids:
            predicted_ids.append(article["id"])
    
    # Check how many results are correct
    correct = 0
    for article_id in predicted_ids:
        if article_id in expected_ids:
            correct += 1
    
    total = len(predicted_ids)
    percentage = correct / total
    
    assert percentage >= 0.95
