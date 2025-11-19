from app.job_processor import get_normalized_name, score_and_filter_candidates

def test_get_normalized_name():
    assert get_normalized_name("Tesla Inc") == "tesla inc"
    assert get_normalized_name("Tata Motors") == "tata motors"    

def test_scoring_exact_match():
    search_terms = {
        "normalized_name": "tesla inc",
        "partial_matches": ["tesla"],
        "industry_keywords": ["electric vehicle", "battery"]
    }
    
    candidates = [
        {"id": "art_001", "title": "Tesla Inc Unveils Revolutionary Solid-State Battery", 
         "snippet": "Tesla Inc announces breakthrough in solid-state battery technology promising 1000km range", 
         "source": "The Economic Times", "published_at": "2025-11-10", 
         "url": "https://grokipedia.com/tesla-battery"}

    ]
    
    results = score_and_filter_candidates(search_terms, candidates)
    
    assert len(results) > 0
    assert results[0]["score"] >= 20  # Exact match gives +20


def test_filtering_low_scores():
    search_terms = {
        "normalized_name": "OLA Inc",
        "partial_matches": ["ola"],
        "industry_keywords": ["electric vehicle"]
    }
    
    candidates = [
        {
            "id": "4",
            "title": "OLA launches new scooter",
            "snippet": "Ola unveils latest electric scooter model at Mumbai event",
            "source": "AANews",
            "published_at": "2025-11-10",
            "url": "http://grokipedia.com/ola-launches-new-scooter"
        }
    ]
    
    results = score_and_filter_candidates(search_terms, candidates)
    
    assert len(results) == 0 
    