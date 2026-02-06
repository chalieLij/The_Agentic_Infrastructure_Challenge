import pytest
from src.skills import analyze_trend

def test_fetch_trends_returns_correct_schema():
    """
    Test that fetch_trends returns data matching the specs/technical.md schema.
    """
    # Act
    # Calling the function which is expected not to exist yet or fail
    response = analyze_trend.fetch_trends(niche="tech", region="US", limit=5)

    # Assert keys match the spec
    assert "timestamp" in response
    assert response["niche"] == "tech"
    assert "trends" in response
    assert isinstance(response["trends"], list)
    
    # Assert trend item structure
    if len(response["trends"]) > 0:
        trend = response["trends"][0]
        assert "rank" in trend
        assert "keyword" in trend
        assert "volume" in trend
        assert "related_hashtags" in trend
        assert "sentiment_score" in trend
        assert isinstance(trend["sentiment_score"], float)
