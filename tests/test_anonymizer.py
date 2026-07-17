from src.detector import PIIDetector
from src.anonymizer import PIIAnonymizer

sample = """
John Doe works at Microsoft.

Email: john.doe@gmail.com

Phone: +91 9876543210

John Doe is a Software Engineer.

Microsoft hired John Doe.
"""

detector = PIIDetector()

entities = detector.detect(sample)

anonymizer = PIIAnonymizer()

mapping = anonymizer.build_mapping(entities)

print("=" * 70)

for original, fake in mapping.items():

    print(f"{original:<25} --> {fake}")