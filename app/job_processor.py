import asyncio
import json
import os

from app.aggregators import FileFixtureAggregator, DummyNewsApiAggregator
from app.config import FIXTURES_DIR, DATA_DIR
from app.utils import *

API_KEY = os.getenv("NEWS_API_KEY")

INDUSTRY_TERMS_PATH = os.path.join(FIXTURES_DIR, "industry_terms.json")
with open(INDUSTRY_TERMS_PATH, "r") as f:
    INDUSTRY_TERMS = json.load(f)

# Multiple Aggregators
FILE_AGGREGATOR = FileFixtureAggregator()
API_AGGREGATOR = DummyNewsApiAggregator()

def get_normalized_name(company_name):
    return company_name.lower().strip()

def get_partial_matches(company_name):
    return company_name.lower().split()

def get_industry_keywords():
    pass

def score_and_filter_candidates(candidates):

    #TODO : Implement scoring and filtering logic
    filtered_candidates = candidates
    return filtered_candidates

def generate_search_terms(company_name):

    normalized_name = get_normalized_name(company_name)
    partial_matches = get_partial_matches(company_name)
    industry_keywords = get_industry_keywords()

    return {
        "normalized_name": normalized_name,
        "partial_matches": partial_matches,
        "industry_keywords": industry_keywords,
    }


async def process_job(job_id: str, company_name: str):
    search_terms = generate_search_terms(company_name)

    print(f"Processing job {job_id} for company '{company_name}'")
    print(f"Generated search terms: {search_terms}")

    if API_KEY:
        print("---> Using News API Aggregator...")
        candidates = API_AGGREGATOR.fetch_candidates(search_terms)
    else:
        print("---> Using File Fixture Aggregator")
        candidates = FILE_AGGREGATOR.fetch_candidates(search_terms)

    print(f"Found {len(candidates)} candidate articles for job {job_id}")

    filtered_candidates = score_and_filter_candidates(candidates)

    print(f"Found {len(filtered_candidates)} filtered candidate articles for job {job_id}")

    result = {
        "job_id": job_id,
        "company_name": company_name,
        "total_candidates": len(candidates),
        "filtered_candidates": filtered_candidates,
    }

    job_dir = get_job_dir(job_id)
    result_path = get_results_path(job_id)
    with open(result_path, "w") as f:
        json.dump(result, f, indent=4)

    # update job status to 'completed' in a real application
    with open(get_request_path(job_id), "r") as f:
        request_data = json.load(f)
        request_data["status"] = "Completed"
    with open(get_request_path(job_id), "w") as f:
        json.dump(request_data, f, indent=4)

    print(f"Job {job_id} processing complete.")