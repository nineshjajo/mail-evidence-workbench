import re
from collections.abc import Iterable

URL_RE = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
HASH_RE = re.compile(r"\b(?:[a-f0-9]{32}|[a-f0-9]{40}|[a-f0-9]{64})\b", re.IGNORECASE)
DOMAIN_RE = re.compile(r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}\b", re.IGNORECASE)


def _unique(values: Iterable[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        cleaned = value.rstrip(".,;:)]}")
        key = cleaned.lower()
        if key not in seen:
            seen.add(key)
            result.append(cleaned)
    return tuple(result)


def extract_indicators(text: str) -> dict[str, tuple[str, ...]]:
    return {
        "urls": _unique(URL_RE.findall(text)),
        "domains": _unique(DOMAIN_RE.findall(text)),
        "ips": _unique(IP_RE.findall(text)),
        "hashes": _unique(HASH_RE.findall(text)),
    }


def authentication_evidence(values: Iterable[str]) -> tuple[str, ...]:
    findings: list[str] = []
    for value in values:
        lowered = value.lower()
        for method in ("spf", "dkim", "dmarc"):
            if f"{method}=fail" in lowered:
                findings.append(f"{method.upper()} reported failure")
            elif f"{method}=pass" in lowered:
                findings.append(f"{method.upper()} reported pass")
    return _unique(findings)
