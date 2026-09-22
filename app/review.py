from .evidence import authentication_evidence
from .models import Evidence, ReviewRecord
from .parser import parse_message
from .providers import ReputationProvider

PRESSURE_PHRASES = ("verify your account", "payment required", "confirm now", "security alert")


def build_review(raw: bytes, provider: ReputationProvider | None = None) -> ReviewRecord:
    message = parse_message(raw)
    evidence: list[Evidence] = []
    body = f"{message.subject}\n{message.text}\n{message.html}".lower()

    auth_findings = authentication_evidence(message.authentication_results)
    for finding in auth_findings:
        evidence.append(Evidence("authentication", finding, "Authentication-Results"))
    if message.urls:
        evidence.append(Evidence("content", f"{len(message.urls)} URL(s) found", "message body"))
    if message.attachments:
        evidence.append(Evidence("attachment", f"{len(message.attachments)} attachment(s) found", "MIME structure"))
    if any(phrase in body for phrase in PRESSURE_PHRASES):
        evidence.append(Evidence("content", "credential or payment-pressure phrase found", "subject/body"))

    if provider and message.domains:
        observation = provider.inspect(message.domains[0])
        evidence.append(Evidence("enrichment", observation.value, observation.source))

    if len(evidence) >= 3:
        suggested_state, confidence = "suspicious", "medium"
    elif evidence:
        suggested_state, confidence = "review", "low"
    else:
        suggested_state, confidence = "no-obvious-signal", "low"

    indicators = {
        "urls": message.urls,
        "domains": message.domains,
        "ips": message.ips,
        "hashes": message.hashes,
    }
    return ReviewRecord(
        subject=message.subject,
        suggested_state=suggested_state,
        confidence=confidence,
        evidence=tuple(evidence),
        indicators=indicators,
    )
