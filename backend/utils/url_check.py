def looks_suspicious(url: str) -> bool:
    return any(x in url for x in ["bit.ly", "tinyurl", "@", "//@", "xn--"])
