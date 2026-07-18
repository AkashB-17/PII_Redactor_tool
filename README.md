# 🛡️ PII Redaction Tool

A modular **Personally Identifiable Information (PII) Redaction Tool** that automatically detects and anonymizes sensitive information from **DOCX** and **PDF** documents.

The project combines **Regex-based pattern matching** with **spaCy Named Entity Recognition (NER)** to identify both structured and unstructured PII while maintaining consistent anonymization using **Faker**.

---

## ✨ Features

- Hybrid PII detection using **Regex + spaCy**
- Consistent anonymization using **Faker**
- Supports:
  - DOCX documents
  - PDF documents *(in progress / implemented depending on your project status)*
- Detects:
  - Full Names
  - Email Addresses
  - Phone Numbers
  - Company Names
  - Physical Addresses
  - Social Security Numbers (SSN)
  - Credit Card Numbers
  - Date of Birth
  - IPv4 Addresses
- Modular architecture
- Easily extensible for new PII types

---

# System Architecture

```text
                    Input Document
                   (DOCX / PDF)
                          │
                          ▼
                 Document Processor
                          │
                          ▼
                  Text Extraction
                          │
                          ▼
              Hybrid Detection Engine
          ┌────────────────────────────┐
          │ Regex Detector             │
          │ spaCy Named Entity Model   │
          └────────────────────────────┘
                          │
                          ▼
             Consistent Anonymization
                    (Faker Mapping)
                          │
                          ▼
               Document Reconstruction
                          │
                          ▼
                 Redacted Document
```

---

# Project Structure

```text
PII_Redaction_Tool/
│
├── data/
│   ├── input/
│   └── output/
│
├── src/
│   ├── detector.py
│   ├── anonymizer.py
│   ├── regex_patterns.py
│   ├── docx_processor.py
│   ├── pdf_processor.py
│   ├── evaluate.py
│   └── utils.py
│
├── tests/
│
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# Detection Pipeline

The system follows a hybrid detection approach.

## 1. Regex Detection

Regex is used for deterministic identification of structured PII.

Examples:

- Email Address
- Phone Number
- Credit Card Number
- SSN
- IPv4 Address
- Date of Birth

Regex provides high precision for structured patterns.

---

## 2. spaCy Named Entity Recognition

spaCy identifies contextual entities such as:

- PERSON
- ORG
- GPE

This improves recall for unstructured PII that cannot be reliably detected using regular expressions.

---

## 3. Consistent Anonymization

Detected entities are replaced using **Faker**.

Example:

```
Onkar Bose

↓

John Doe
```

The same entity is always mapped to the same replacement throughout the document.

---

# Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/PII_Redaction_Tool.git

cd PII_Redaction_Tool
```

Install dependencies

```bash
uv sync
```

Install the spaCy model

```bash
uv run python -m spacy download en_core_web_sm
```

---

# Usage

Place your input document inside

```
data/input/
```

Run

```bash
uv run python -m tests.test_docx
```

The redacted document will be generated in

```
data/output/
```

---

# Supported PII Types

| Entity | Detection Method |
|----------|-----------------|
| Person Name | spaCy |
| Organization | spaCy |
| Email | Regex |
| Phone Number | Regex |
| SSN | Regex |
| Credit Card | Regex |
| IPv4 Address | Regex |
| Date of Birth | Regex |

---

# Evaluation Methodology

This project distinguishes between **offline evaluation** and **production evaluation**.

## Offline Evaluation

Precision, Recall and F1-score are computed only when a manually annotated ground truth is available.

Detector predictions are compared against the labeled entities.

This follows standard Named Entity Recognition (NER) evaluation methodology.

---

## Production Evaluation

For arbitrary user-uploaded documents, no labeled ground truth exists.

Therefore, true Precision, Recall and F1-score cannot be computed.

Instead, production systems should report operational metrics such as:

- Total PII entities detected
- Entity distribution
- Replacement success rate
- Leakage count
- Processing time

This reflects common production monitoring practices for NLP systems.

---

# Trade-offs

## Ground Truth Dependency

Precision, Recall and F1-score require manually labeled data.

They cannot be computed reliably for arbitrary user-uploaded documents.

---

## Hybrid Detection

Regex provides high precision for structured entities.

spaCy improves recall for contextual entities but may occasionally over-detect organization names.

---

## Document Support

Current implementation focuses on digital DOCX/PDF documents.

OCR-based scanned PDFs are outside the current scope.

---

## Formatting

Basic document formatting is preserved where possible.

Support for complex objects (text boxes, embedded shapes, SmartArt) can be extended in future versions.

---

# Future Improvements

- Microsoft Presidio Integration
- OCR Support (Tesseract / PaddleOCR)
- Transformer-based NER Models
- Confidence Thresholding
- Human-in-the-loop Review
- Batch Processing
- REST API
- Docker Deployment
- Audit Logging
- Secure File Deletion

---

# Technologies Used

- Python
- spaCy
- Faker
- python-docx
- PyMuPDF
- UV
- Regex

---

# License

This project was developed as part of a technical assessment for automated PII redaction and is intended for educational and evaluation purposes.
