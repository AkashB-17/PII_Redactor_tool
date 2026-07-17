"""
PII Anonymizer

Generates fake replacements while maintaining
consistent mappings across the document.
"""

from __future__ import annotations

from faker import Faker

from src.utils import DetectedEntity


class PIIAnonymizer:

    def __init__(self):

        self.fake = Faker()

        # Original -> Fake
        self.mapping = {}

    # ----------------------------------------------------
    # Fake Value Generator
    # ----------------------------------------------------

    def _generate_fake(self, entity: DetectedEntity) -> str:

        entity_type = entity.entity_type

        if entity_type == "PERSON":
            return self.fake.name()

        elif entity_type == "EMAIL":
            return self.fake.email()

        elif entity_type == "PHONE":
            return self.fake.phone_number()

        elif entity_type == "ORG":
            return self.fake.company()

        elif entity_type == "GPE":
            return self.fake.city()

        elif entity_type == "IP_ADDRESS":
            return self.fake.ipv4()

        elif entity_type == "SSN":
            return self.fake.ssn()

        elif entity_type == "CREDIT_CARD":
            return self.fake.credit_card_number()

        elif entity_type == "DATE_OF_BIRTH":
            return str(self.fake.date_of_birth())

        # Unknown entity
        return "<REDACTED>"

    # ----------------------------------------------------
    # Mapping Builder
    # ----------------------------------------------------

    def build_mapping(self, entities: list[DetectedEntity]) -> dict[str, str]:

        for entity in entities:

            if entity.value not in self.mapping:

                self.mapping[entity.value] = self._generate_fake(entity)

        return self.mapping