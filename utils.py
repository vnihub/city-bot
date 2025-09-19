# utils.py
import aiohttp, asyncio, os

_TINY_API = "https://api.tinyurl.com/create"
_API_KEY = os.getenv("TINYURL_API_TOKEN")

async def tiny(url: str, retries: int = 3, timeout: int = 2) -> str:
    """
    Return a TinyURL-shortened link, or the original URL on failure.

    Parameters
    ----------
    url : str
        The URL to shorten.
    retries : int
        How many times to retry on error (default 3).
    timeout : int
        Per-request timeout in seconds (default 2).
    """
    if not _API_KEY:
        print("⚠️ TinyURL API key not found, returning original URL.")
        return url

    if len(url) < 30:
        return url

    headers = {
        "Authorization": f"Bearer {_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"url": url}

    for attempt in range(1, retries + 1):
        try:
            async with aiohttp.ClientSession() as sess:
                async with sess.post(_TINY_API, headers=headers, json=payload, timeout=timeout) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("data", {}).get("tiny_url", url)
        except Exception:
            if attempt < retries:
                await asyncio.sleep(0.2)
            else:
                break

    return url