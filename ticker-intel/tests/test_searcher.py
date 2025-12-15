import os
import respx
import httpx

from ticker_intel.searcher import serper_search, SERPER_ENDPOINT

@respx.mock
def test_serper_search_parses_organic(monkeypatch):
    monkeypatch.setenv("SERPER_API_KEY", "test-key")

    respx.post(SERPER_ENDPOINT).mock(
        return_value=httpx.Response(
            200,
            json={
                "organic": [
                    {"title": "A", "link": "https://example.com/a", "snippet": "x", "position": 1},
                    {"title": "B", "link": "https://example.com/b", "snippet": "y", "position": 2},
                ]
            },
        )
    )

    results = serper_search("apple", num=10)
    assert len(results) == 2
    assert results[0].link == "https://example.com/a"


@respx.mock
def test_serper_search_sends_api_key_header(monkeypatch):
    monkeypatch.setenv("SERPER_API_KEY", "test-key")

    route = respx.post(SERPER_ENDPOINT).mock(
        return_value=httpx.Response(200, json={"organic": []})
    )

    _ = serper_search("apple", num=10)

    assert route.called
    sent_key = route.calls[0].request.headers.get("X-API-KEY")
    assert sent_key == "test-key"
