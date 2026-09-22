# Mail Evidence Workbench

A portfolio-safe reimplementation of a local email-evidence workbench. It demonstrates how a review tool can parse a synthetic `.eml`, collect observable evidence, and generate an analyst-facing review record without making an automatic final decision.

This repository is **not a copy of any internal or employer-owned application**. It contains no company code, customer data, proprietary headers, internal rule IDs, private endpoints, credentials, or production samples. The fixture is synthetic.

## What it demonstrates

- Generic RFC/MIME parsing
- Authentication-Results inspection
- URL, domain, IP, and hash extraction
- Explainable evidence collection
- A provider interface for public reputation enrichment
- Human-in-the-loop review records
- JSON output suitable for a future Flask UI

## Run it

```text
python -m venv .venv
.venv\\Scripts\\activate       # Windows
pip install -e .
python run.py samples/synthetic_review.eml
```

The command performs no network requests. Optional enrichment is represented by a mock provider so the demo is deterministic and safe to publish.

## Safety boundary

The original internal project that inspired this demo is not included. Do not add employer code, internal header formats, customer `.eml` files, case numbers, private infrastructure, credentials, logs, databases, or proprietary rule data. Review your employment and intellectual-property obligations before publishing.

## Layout

```text
app/
  evidence.py      Generic observable-evidence extraction
  models.py        Public data structures
  parser.py        RFC/MIME parsing
  providers.py     Mock, replaceable enrichment provider
  review.py        Human-review record builder
samples/           Synthetic fixture only
tests/            Unit tests
run.py            CLI entry point
```
