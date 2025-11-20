
import json
import os

from app.config import FIXTURES_DIR

class FileFixtureAggregator():

    def __init__(self):
        self.file_path = os.path.join(FIXTURES_DIR, "news_sample.jsonl")

    def published_at_withinduration(self, published_at: str, duration: int):
        if not published_at:
            return False
        from datetime import datetime, timedelta
        published_date = datetime.strptime(published_at, "%Y-%m-%d")
        current_date = datetime.now()
        duration_delta = timedelta(days=duration*30) #duration in months approximated to days
        return current_date - published_date <= duration_delta
        
    def fetch_candidates(self, search_terms: dict, duration: int):
        candidates = []
        with open(self.file_path, "r") as f:
            for line in f:
                candidate_data = json.loads(line)
                if candidate_data and self.published_at_withinduration(candidate_data.get("published_at"), duration):
                    candidates.append(candidate_data)
        print(f"Loaded {len(candidates)} candidates from fixture file.")
        return candidates

class DummyNewsApiAggregator():

    def __init__(self):
        pass

    def fetch_candidates(self, search_terms, duration):
        candidates = []
        candidates.append(
                {"id" : 1, 
                 "title": "Testing", 
                 "published_at": "2024-01-01", 
                 "source": "Testing Testing", 
                 "url": "http://test.com", 
                 "snippet": "Sample Testing"})
        return candidates