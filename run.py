import argparse
import json
from pathlib import Path

from app.providers import MockReputationProvider
from app.review import build_review


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a human-review record from a synthetic EML.")
    parser.add_argument("eml", type=Path)
    args = parser.parse_args()
    result = build_review(args.eml.read_bytes(), provider=MockReputationProvider())
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
