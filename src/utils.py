from dataclasses import dataclass

@dataclass
class DetectedEntity:
    entity_type: str
    value: str
    start: int
    end: int