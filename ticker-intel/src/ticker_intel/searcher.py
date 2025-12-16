import os
import httpx
from ticker_intel.models import SearchHit

# define constants
SERPER_ENDPOINT = "https://google.serper.dev/search"

# load API key from environment variable
serper_api_key = os.getenv("SERPER_API_KEY")
if not serper_api_key:
        raise RuntimeError("Missing SERPER_API_KEY environment variable")


def serper_search(query: str, *, num: int = 10) -> list[SearchHit]:
    """
    Perform a search using the Serper API and return a list of SearchHit objects.
    """
    
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "q": query,
        "num": num,
    }

    with httpx.Client(timeout=10.0) as client:
        resp = client.post(SERPER_ENDPOINT, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
    print(f"Serper raw response data: {data}\n\n")
    organic = data.get("organic", [])
    print(f"Serper raw response organic data: {organic}\n\n")
    hit = [
        SearchHit(
            title=item["title"],
            link=item["link"],
            snippet=item.get("snippet"),
            position=item.get("position"),
        )
        for item in organic
    ]
    return hit