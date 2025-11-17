
import json
import os

from app.config import FIXTURES_DIR

class FileFixtureAggregator():

    def __init__(self):
        self.file_path = os.path.join(FIXTURES_DIR, "news_sample.jsonl")

    def fetch_candidates(self, search_terms: dict):
        candidates = []
        candidates.append(
                {"id" : 1, 
                 "title": "Testing", 
                 "published_at": "2024-01-01", 
                 "source": "Testing Testing", 
                 "url": "http://test.com", 
                 "snippet": "Sample Testing"})
        return candidates

class DummyNewsApiAggregator():

    def __init__(self):
        pass

    def fetch_candidates(self, search_terms: dict):
        candidates = []
        candidates.append(
                {"id" : 1, 
                 "title": "Testing", 
                 "published_at": "2024-01-01", 
                 "source": "Testing Testing", 
                 "url": "http://test.com", 
                 "snippet": "Sample Testing"})
        return candidates