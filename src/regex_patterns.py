"""
Regex patterns for structured PII detection.
"""

EMAIL_PATTERN = (
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

# International phone numbers (10–15 digits)
PHONE_PATTERN = (
    r"\b(?:\+\d{1,3}[- ]?)?\d{10,15}\b"
)

SSN_PATTERN = (
    r"\b\d{3}-\d{2}-\d{4}\b"
)

CREDIT_CARD_PATTERN = (
    r"\b(?:\d{4}[- ]?){3}\d{4}\b"
)

IPV4_PATTERN = (
    r"\b(?:25[0-5]|2[0-4]\d|1?\d?\d)"
    r"(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}\b"
)

DOB_PATTERN = (
    r"\b(?:"
    r"\d{2}[/-]\d{2}[/-]\d{4}"
    r"|"
    r"\d{4}[/-]\d{2}[/-]\d{2}"
    r")\b"
)