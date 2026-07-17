from src.docx_processor import DocxProcessor
from src.evaluate import AutomatedEvaluator

# 1. Define the specific answer key for this document
GROUND_TRUTH = [
    "Onkar Bose", "Tarak Dasgupta", "Harita Jha", "Samaksh Savant", "Pingle LLC",
    "dalalkiaan@example.com", "quincy72@example.org",
    "+ 91 20 45053237",
    "VISHAL SINGH", "SUGRIV SINGH", "06/05/2000", "NBWPS1951N",
    "MERAJ KHAN", "Sudhdan Khan", "12/12/1988", "2943 6593 3461"
]

INPUT_FILE = "data/input/Red Herring Prospectus.docx"
OUTPUT_FILE = "data/output/Red Herring Prospectus_Redacted.docx"

# 2. Run the pipeline
processor = DocxProcessor()
processor.process(input_path=INPUT_FILE, output_path=OUTPUT_FILE)

# 3. Automate the file diffing and evaluation
metrics = AutomatedEvaluator.evaluate(
    input_path=INPUT_FILE,
    output_path=OUTPUT_FILE,
    actual_replacements=processor.anonymizer.mapping,
    ground_truth=GROUND_TRUTH
)

print("\n" + "=" * 50)
print("AUTOMATED EVALUATION REPORT")
print("=" * 50)
for metric, value in metrics.items():
    print(f"{metric:<20}: {value}")