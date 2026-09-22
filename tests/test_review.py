from app.providers import MockReputationProvider
from app.review import build_review


def test_review_is_explainable_and_pending() -> None:
    raw = b"From: sender@example.test\nSubject: Security alert\nAuthentication-Results: example.test; spf=fail\n\nhttps://portal.example.test"
    result = build_review(raw, provider=MockReputationProvider())
    assert result.suggested_state == "suspicious"
    assert result.final_state == "pending-human-review"
    assert result.evidence
    assert result.indicators["urls"] == ("https://portal.example.test",)
