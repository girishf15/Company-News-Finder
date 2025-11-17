
import json
import os

from app.config import FIXTURES_DIR

class FileFixtureAggregator():

    def __init__(self):
        self.file_path = os.path.join(FIXTURES_DIR, "news_sample.jsonl")

    def fetch_candidates(self, search_terms: dict):
        candidates = []
        return candidates

class DummyNewsApiAggregator():

    def __init__(self):
        pass

    def fetch_candidates(self, search_terms: dict):
        candidates = []
        return candidates