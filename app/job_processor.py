import asyncio
import json
import os

from app.aggregators import FileFixtureAggregator, DummyNewsApiAggregator
from app.config import FIXTURES_DIR

API_KEY = os.getenv("NEWS_API_KEY")

INDUSTRY_TERMS_PATH = os.path.join(FIXTURES_DIR, "industry_terms.json")
with open(INDUSTRY_TERMS_PATH, "r") as f:
    INDUSTRY_TERMS = json.load(f)

# Multiple Aggregators
FILE_AGGREGATOR = FileFixtureAggregator()
API_AGGREGATOR = DummyNewsApiAggregator()

def get_partial_matches():
    pass

def get_normalized_name():
    pass

def get_industry_keywords():
    pass

def score_and_filter_candidates():
    pass

def generate_search_terms(company_name):

    normalized_name = get_normalized_name()
    partial_matches = get_partial_matches()
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

    filtered_candidates = score_and_filter_candidates()

    print(f"Found {len(filtered_candidates)} filtered candidate articles for job {job_id}")
