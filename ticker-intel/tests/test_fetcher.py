import httpx
import respx

from ticker_intel.fetcher import fetch_url


@respx.mock
def test_fetch_url_returns_sourcedoc_and_normalizes_text():
    # Arrange
    url = "https://example.com/page"
    noisy = "a   b\n\n\nc"
    respx.get(url).mock(
        return_value=httpx.Response(
            200,
            text=noisy,
            headers={"Content-Type": "text/html; charset=utf-8"},
        )
    )

    # Act
    doc = fetch_url(url)

    # Assert
    assert doc.url == url
    assert doc.title is None
    assert doc.content_text == "a b\n\nc"
    assert doc.retrieved_at is not None


@respx.mock
def test_fetch_url_retries_on_500_then_succeeds(monkeypatch):
    # Arrange
    url = "https://example.com/flaky"

    # Volitelně: zrychli test (pokud ve fetcheru používáš time.sleep)
    # 1) pokud máš ve fetcher.py "import time" a pak "time.sleep(...)"
    # tak jde přepatchovat takhle:
    import ticker_intel.fetcher as fetcher_module
    monkeypatch.setattr(fetcher_module.time, "sleep", lambda _: None)

    route = respx.get(url)
    route.side_effect = [
        httpx.Response(500, text="server error"),
        httpx.Response(200, text="ok"),
    ]

    # Act
    doc = fetch_url(url)

    # Assert
    assert doc.url == url
    assert doc.content_text == "ok"
    assert route.called
    assert len(route.calls) == 2
