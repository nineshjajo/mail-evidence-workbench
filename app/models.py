from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Message:
    sender: str
    recipients: tuple[str, ...]
    subject: str
    text: str
    html: str
    authentication_results: tuple[str, ...]
    urls: tuple[str, ...]
    domains: tuple[str, ...]
    ips: tuple[str, ...]
    hashes: tuple[str, ...]
    attachments: tuple[str, ...]


@dataclass(frozen=True)
class Evidence:
    category: str
    observation: str
    source: str


@dataclass(frozen=True)
class ReviewRecord:
    subject: str
    suggested_state: str
    confidence: str
    evidence: tuple[Evidence, ...] = field(default_factory=tuple)
    indicators: dict[str, tuple[str, ...]] = field(default_factory=dict)
    final_state: str = "pending-human-review"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
