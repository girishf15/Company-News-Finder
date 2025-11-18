import asyncio
import json
import os

from app.aggregators import FileFixtureAggregator, DummyNewsApiAggregator
from app.config import FIXTURES_DIR, DATA_DIR, STATUS_COMPLETED, STATUS_FAILED, THRESHOLD_SCORE
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
    partial_matches = []
    suffixes = ["inc", "llc", "ltd", "corp","org", "industries", "pvt", "private", "limited"]
    name_parts = company_name.lower().split()
    for each_part in name_parts:
        if each_part not in suffixes:
            partial_matches.append(each_part)        

    return partial_matches


def get_industry_keywords(normalized_name):
    for industry, keywords in INDUSTRY_TERMS.items():
        if industry in normalized_name:
            return keywords
    return []


def score_and_filter_candidates(search_terms, candidates):

    filtered_candidates = []

    for each_article in candidates:
        score = 0
        matched_terms = []
        reasons = []
        
        title = each_article.get("title","").lower()
        snippet = each_article.get("snippet","").lower()

        company_name = search_terms["normalized_name"]
        partial_matches = search_terms["partial_matches"]
        industry_keywords = search_terms["industry_keywords"]


        # Exact match
        if company_name in title or company_name in snippet:
            score += 20
            reasons.append("Exact name match found - Score +20")

        #partial matches
        partial_score = 0
        for part in partial_matches:
            if part in title or part in snippet:
                partial_score += 2

        if partial_score > 0:
            reasons.append("Partial match found - Score +" + str(min(partial_score, 10)))

        #industry keywords
        industry_terms_score = 0
        for keyword in industry_keywords:
            if keyword in title or keyword in snippet:
                industry_terms_score += 2

        if industry_terms_score > 0:
            reasons.append("Industry keyword match found - Score +" + str(min(industry_terms_score, 10)))
        
        score += min(partial_score, 10) + min(industry_terms_score, 10)
        
        if score >= THRESHOLD_SCORE:
            #update article with score, matched_terms, and reasons
            each_article["score"] = score
            each_article["reasons"] = reasons
            filtered_candidates.append(each_article)
        else:
            print(f"Article '{each_article.get('title')}' filtered out with score {score}")

    return filtered_candidates

def generate_search_terms(company_name: str):

    normalized_name = get_normalized_name(company_name)
    partial_matches = get_partial_matches(company_name)
    industry_keywords = get_industry_keywords(normalized_name)

    return {
        "normalized_name": normalized_name,
        "partial_matches": partial_matches,
        "industry_keywords": industry_keywords,
    }


async def process_job(job_id: str, company_name: str, duration: int):

    try:
        search_terms = generate_search_terms(company_name)

        print(f"Processing job {job_id} for company '{company_name}'")
        print(f"Generated search terms: {search_terms}")

        if API_KEY:
            print("---> Using News API Aggregator...")
            candidates = API_AGGREGATOR.fetch_candidates(search_terms, duration)
        else:
            print("---> Using File Fixture Aggregator")
            candidates = FILE_AGGREGATOR.fetch_candidates(search_terms, duration)

        print(f"Found {len(candidates)} total candidate articles for job {job_id}")

        filtered_candidates = score_and_filter_candidates(search_terms, candidates)
        print(f"Found {len(filtered_candidates)} filtered_candidates candidate articles for job {job_id}")

        # Save raw candidates to candidates.jsonl
        candidates_path = get_candidates_path(job_id)
        with open(candidates_path, "w") as f:
            for candidate in candidates:
                f.write(json.dumps(candidate) + "\n")
        
        # Save filtered candidates to filtered.jsonl
        filtered_path = get_filtered_path(job_id)
        with open(filtered_path, "w") as f:
            for candidate in filtered_candidates:
                f.write(json.dumps(candidate) + "\n")

        result = {
            "job_id": job_id,
            "company_name": company_name,
            "total_candidates": len(candidates),
            "filtered_candidates": filtered_candidates,
        }

        result_path = get_results_path(job_id)
        with open(result_path, "w") as f:
            json.dump(result, f, indent=4)

        # update job status to 'completed'
        update_job_status(job_id, STATUS_COMPLETED)
        print(f"Job {job_id} processing complete.")
    except Exception as e:
        print(f"Error processing job {job_id}: {e}")
        update_job_status(job_id, STATUS_FAILED)