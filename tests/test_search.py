from backend.app.services.search import search

def test_search_response():
    query = "test"
    results = search(query, top_k=3)
    assert isinstance(results, list)
    if results:
        assert "text" in results[0]
        assert "metadata" in results[0]
        assert "score" in results[0]
