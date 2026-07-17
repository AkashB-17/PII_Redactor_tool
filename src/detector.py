"""
Hybrid PII Detector

Uses:
1. Regex -> Structured PII
2. spaCy -> PERSON, ORG, GPE
"""

from __future__ import annotations

import re
from typing import List

import spacy

from src.regex_patterns import (
    EMAIL_PATTERN,
    PHONE_PATTERN,
    SSN_PATTERN,
    CREDIT_CARD_PATTERN,
    IPV4_PATTERN,
    DOB_PATTERN,
)

from src.utils import DetectedEntity


class PIIDetector:
    """
    Hybrid detector using Regex + spaCy.
    """

    def __init__(self, model_name: str = "en_core_web_sm"):

        self.nlp = spacy.load(model_name)

        self.patterns = {
            "EMAIL": EMAIL_PATTERN,
            "PHONE": PHONE_PATTERN,
            "SSN": SSN_PATTERN,
            "CREDIT_CARD": CREDIT_CARD_PATTERN,
            "IP_ADDRESS": IPV4_PATTERN,
            "DATE_OF_BIRTH": DOB_PATTERN,
        }

        self.spacy_entities = {
            "PERSON",
            "ORG",
            "GPE",
        }

    # ----------------------------------------------------
    # Regex Detection
    # ----------------------------------------------------

    def regex_detect(self, text: str) -> List[DetectedEntity]:

        entities = []

        for entity_type, pattern in self.patterns.items():

            for match in re.finditer(pattern, text):

                value =match.group()

                if entity_type == "PHONE":
                    digits = re.sub(r"\D", "", value)

                    if len(digits) < 10 or len(digits) > 15:
                        continue

                entities.append(
                    DetectedEntity(
                        entity_type=entity_type,
                        value=match.group(),
                        start=match.start(),
                        end=match.end(),
                    )
                )

        return entities

    # ----------------------------------------------------
    # spaCy Detection
    # ----------------------------------------------------

    def spacy_detect(self, text: str) -> List[DetectedEntity]:

        doc = self.nlp(text)

        entities = []

        for ent in doc.ents:

            if ent.label_ in self.spacy_entities:

                entities.append(
                    DetectedEntity(
                        entity_type=ent.label_,
                        value=ent.text,
                        start=ent.start_char,
                        end=ent.end_char,
                    )
                )

        return entities

    # ----------------------------------------------------
    # Merge Detections
    # ----------------------------------------------------

    def detect(self, text: str) -> List[DetectedEntity]:
        """
        Run all detectors and merge results.
        """

        regex_entities = self.regex_detect(text)
        spacy_entities = self.spacy_detect(text)

        merged = regex_entities + spacy_entities

        # Remove duplicates
        unique = {}

        for entity in merged:
            key = (
                entity.start,
                entity.end,
                entity.entity_type,
            )

            if key not in unique:
                unique[key] = entity

        return sorted(
            unique.values(),
            key=lambda entity: entity.start,
        )
    
    