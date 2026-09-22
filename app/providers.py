from dataclasses import dataclass


@dataclass(frozen=True)
class ReputationObservation:
    subject: str
    value: str
    source: str = "mock-provider"


class ReputationProvider:
    """Replaceable interface; a public demo never calls an internal service."""

    def inspect(self, domain: str) -> ReputationObservation:
        raise NotImplementedError


class MockReputationProvider(ReputationProvider):
    def inspect(self, domain: str) -> ReputationObservation:
        return ReputationObservation(
            subject=domain,
            value="not-evaluated; replace this provider with an authorized public service",
        )
