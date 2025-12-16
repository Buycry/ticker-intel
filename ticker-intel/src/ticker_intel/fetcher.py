from datetime import datetime, timezone
import time
import httpx

from ticker_intel.models import SourceDoc
from ticker_intel.text import normalize_text

DEFAULT_TIMEOUT = 10.0
MAX_RETRIES = 3
BACKOFF_SECONDS = [0.5, 1.0, 2.0]

def fetch_url(url: str) -> SourceDoc:
    headers = {"User-Agent": "ticker-intel/0.1 (+https://github.com/Buycry/ticker-intel)"}

    last_exc: Exception | None = None

    with httpx.Client(timeout=DEFAULT_TIMEOUT, follow_redirects=True) as client:
        for attempt in range(MAX_RETRIES):
            try:
                resp = client.get(url, headers=headers)
                if resp.status_code == 429 or 500 <= resp.status_code <= 599:
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(BACKOFF_SECONDS[attempt])
                        continue
                    resp.raise_for_status()

                resp.raise_for_status()

                text = normalize_text(resp.text)
                return SourceDoc(
                    url=url,
                    title=None,
                    retrieved_at=datetime.now(timezone.utc),
                    content_text=text,
                )

            except (httpx.TimeoutException, httpx.ConnectError) as e:
                last_exc = e
                if attempt < MAX_RETRIES - 1:
                    time.sleep(BACKOFF_SECONDS[attempt])
                    continue
                raise

    if last_exc:
        raise last_exc
    raise RuntimeError("fetch_url failed unexpectedly")
