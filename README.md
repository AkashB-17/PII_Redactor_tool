# PII Redaction Tool

A modular tool for detecting and anonymizing Personally Identifiable Information (PII) in DOCX and PDF documents. It combines regex-based pattern matching for structured PII with spaCy Named Entity Recognition for unstructured PII, and replaces every detected instance with a consistent, realistic fake value via Faker — so a redacted document reads naturally rather than being full of `[REDACTED]` placeholders.

Built and evaluated against a real-world Red Herring Prospectus (RHP), a dense financial/legal document that exercises PII detection in a genuinely hard setting: mixed paragraph and table layouts, promoter/director tables, registrar and banker contact blocks, and hundreds of pages of legal boilerplate that resembles PII without being PII.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [CLI / Script Processing](#cli--script-processing)
  - [Web UI (Streamlit)](#web-ui-streamlit)
- [Detection Pipeline](#detection-pipeline)
- [Evaluation](#evaluation)
- [Known Limitations](#known-limitations)
- [Deployment](#deployment)
- [Roadmap](#roadmap)

---

## Features

- Hybrid detection: regex for structured PII, spaCy NER for unstructured PII
- Consistent anonymization — the same real value maps to the same fake value everywhere it appears in a document
- Supports both DOCX and PDF input
- Processes paragraphs **and** table cells (most PII in structured documents lives in tables)
- Detects:
  - Full names
  - Company / organization names
  - Email addresses
  - Phone numbers
  - Physical / mailing addresses (partial — see [Known Limitations](#known-limitations))
  - Social Security Numbers (SSN)
  - PAN and Aadhaar numbers (India-specific identifiers)
  - Credit card numbers
  - Dates of birth
  - IPv4 addresses
- Modular, easily extensible architecture
- Scoped evaluation harness with precision/recall/F1 reporting
- Streamlit web UI for interactive upload → redact → download

---

## Architecture

```
                Input Document
               (DOCX / PDF)
                     │
                     ▼
            Document Processor
         (DocxProcessor / PdfProcessor)
                     │
                     ▼
             Text Extraction
        (paragraphs + table cells)
                     │
                     ▼
         Hybrid Detection Engine
    ┌─────────────────────────────┐
    │  Regex Detector              │
    │  (email, phone, SSN, PAN,    │
    │   Aadhaar, credit card, IP,  │
    │   date of birth)             │
    │                              │
    │  spaCy NER                   │
    │  (PERSON, ORG, GPE)          │
    └─────────────────────────────┘
                     │
                     ▼
        Consistent Anonymization
       (Faker-backed mapping, keyed
        by original value)
                     │
                     ▼
         Document Reconstruction
      (in-place run/text replacement,
       structure and tables preserved)
                     │
                     ▼
            Redacted Document
```

---

## Project Structure

```
PII_Redactor_tool/
│
├── data/
│   ├── input/              # source documents (gitignored)
│   └── output/             # redacted documents (gitignored)
│
├── src/
│   ├── detector.py         # hybrid regex + spaCy detection
│   ├── anonymizer.py       # Faker-backed consistent fake-value mapping
│   ├── regex_patterns.py   # all structured-PII regex patterns
│   ├── docx_processor.py   # DOCX read → detect → redact → write
│   ├── pdf_processor.py    # PDF read → detect → redact → write
│   ├── evaluate.py         # scoped precision/recall/F1 evaluation
│   └── utils.py            # shared data model (DetectedEntity)
│
├── tests/
│   ├── test_detector.py
│   ├── test_anonymizer.py
│   ├── test_docx.py
│   ├── test_pdf.py
│   └── test_evaluator.py
│
├── app.py                  # Streamlit web UI
├── main.py
├── requirements.txt         # for platforms that don't read pyproject.toml/uv.lock
├── render.yaml              # Render deployment blueprint
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
git clone https://github.com/AkashB-17/PII_Redactor_tool.git
cd PII_Redactor_tool
uv sync
```

`uv sync` installs all dependencies, including the `en_core_web_sm` spaCy model, which is pinned as a direct wheel URL in `pyproject.toml`.

If you're using plain `pip` instead of `uv` (e.g., on a deployment platform that doesn't support `uv`/`pyproject.toml`):

```bash
pip install -r requirements.txt
```

---

## Usage

### CLI / Script Processing

Place your input document in `data/input/`, then run:

```bash
uv run python -m tests.test_docx
```

The redacted document is written to `data/output/`.

### Web UI (Streamlit)

```bash
uv run streamlit run app.py
```

Open `http://localhost:8501`, upload a `.docx` or `.pdf`, click **Redact Document**, and download the result directly from the browser. See [Deployment](#deployment) for hosting this publicly.

---

## Detection Pipeline

### 1. Regex Detection — structured PII

Deterministic, pattern-based detection for PII with a fixed format: email, phone number, credit card number (with digit-count guarding), SSN, PAN, Aadhaar, IPv4 address, and date-of-birth-shaped dates. Regex gives high precision on these categories since the format itself is the signal.

### 2. spaCy NER — unstructured PII

`en_core_web_sm` identifies contextual entities that have no fixed pattern:

- `PERSON` → full names
- `ORG` → company / organization names
- `GPE` → place names (partial signal toward addresses)

An explicit `ignore_list` in `detector.py` filters out recurring legal/financial boilerplate that spaCy tends to mistag as an organization (e.g., "Board," "Registrar of Companies," "Anchor Investors") — necessarily an incomplete list, since this class of document has a long tail of institution-sounding phrases that aren't real companies.

### 3. Consistent Anonymization

Every detected entity is replaced using Faker, with a persistent mapping from original value → fake value:

```
Onkar Bose  →  John Doe
```

The same real value always produces the same fake value throughout the document, so a redacted document reads as if it were about one consistent set of fictional people and organizations rather than a different fake identity on every mention.

---

## Evaluation

Precision and recall for an entity-extraction task are only meaningful when checked against a ground truth that's **exhaustive** for the text being scored. Hand-labeling every PII instance across an entire ~12,000-line document isn't practical, so evaluation is deliberately **scoped**: a specific, fully-labeled set of document blocks (paragraphs/table cells) is chosen, and both the recall check and the false-positive check are restricted to exactly those blocks — false positives are computed by re-running the detector on the scoped text directly, not by diffing against the whole document's replacement mapping.

| Metric | Definition |
|---|---|
| Precision | TP / (TP + FP) |
| Recall | TP / (TP + FN) |
| F1-Score | Harmonic mean of precision and recall |
| Accuracy (entity-level) | TP / (TP + FP + FN) |

Run the evaluation:

```bash
uv run python -m tests.test_evaluator
```

See `SUBMISSION.md` for the full evaluation methodology write-up and the results table for this document.

---

## Known Limitations

- **Address detection is partial.** Only individual `GPE` place-name tokens are tagged; there is no block-level merge into full contiguous mailing addresses (e.g., anchoring on a 6-digit Indian PIN code and expanding backward to the enclosing address chunk).
- **spaCy over-detects on legal boilerplate.** Generic institutional phrases ("Board," "Corporate Office," "the Government of India") are occasionally mistagged as `ORG`/`GPE`. The `ignore_list` mitigates this but is not exhaustive.
- **Phone number regex has no checksum equivalent to Luhn.** Credit card numbers are validated with a Luhn check; phone numbers rely on digit-count heuristics alone, which can occasionally over- or under-match.
- **Names in unusual formatting may be missed.** All-caps table headers and heavily abbreviated name forms reduce spaCy's contextual signal.
- **PDF redaction is text-overlay based**, not OCR-aware — scanned/image-only PDFs are out of scope for the current implementation.

---

## Deployment

### Streamlit Community Cloud

1. Ensure `requirements.txt` is present at the repo root (Streamlit Cloud reads this, not `pyproject.toml`/`uv.lock`).
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app → select this repo, branch `main`, main file `app.py`.
3. Deploy. First build takes a few minutes due to the spaCy model download.

### Render

A `render.yaml` blueprint is included for one-click setup:

```yaml
services:
  - type: web
    name: pii-redactor-tool
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.0
```

Or configure manually via the Render dashboard using the same build/start commands. Note: Render's free tier spins down on inactivity, so the first request after idle time will have a cold-start delay.

---

## Roadmap

- Microsoft Presidio integration as an alternative/complementary detection backend
- OCR support (Tesseract / PaddleOCR) for scanned PDFs
- Transformer-based NER for improved recall on names and organizations
- Confidence thresholding and human-in-the-loop review for borderline detections
- Contiguous address-block extraction
- REST API and Docker packaging
- Audit logging and secure temporary-file deletion

---

## Tech Stack

Python · spaCy · Faker · python-docx · PyMuPDF · Streamlit · uv

---

## About

Developed as part of a technical assessment for automated PII redaction. Intended for educational and evaluation purposes.