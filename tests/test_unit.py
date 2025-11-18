from app.job_processor import get_normalized_name, get_partial_matches

def test_get_normalized_name():
    result = get_normalized_name("Tesla Inc")
    assert result == "tesla inc"
    

def test_get_partial_matches():
    result = get_partial_matches("Tesla Inc")
    
    assert "tesla" in result
    assert "inc" not in result
    