from src.detector import PIIDetector

sample = """
John Doe works at Microsoft.

Email: john.doe@gmail.com

Phone: +91 9876543210

SSN: 123-45-6789

Credit Card: 1234 5678 9012 3456

Server IP: 192.168.1.100

DOB: 12/06/1999

Address:
One Microsoft Way,
Redmond,
Washington
"""

detector = PIIDetector(model_name="en_core_web_sm")

entities = detector.detect(sample)

print("=" * 70)
print("Detected Entities")
print("=" * 70)

for entity in entities:
    print(entity)