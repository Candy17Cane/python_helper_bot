from services.content_service import search

def test_search_returns_results():
    res = search("класс", limit=5)
    assert isinstance(res, list)

def test_search_empty():
    res = search("")
    assert res == []