from src.docx_processor import DocxProcessor
from src.evaluate import AutomatedEvaluator

INPUT_FILE = "data/input/Red Herring Prospectus.docx"
OUTPUT_FILE = "data/output/Red Herring Prospectus_Redacted.docx"

# ----------------------------------------------------------------------
# STEP 1 (one-time, manual): find out how many text blocks you need to
# read through to label a scope exhaustively. Uncomment and run this on
# its own first, pick a scope_blocks value, then comment it back out.
# ----------------------------------------------------------------------
# AutomatedEvaluator.preview_blocks(INPUT_FILE, n=80)

# ----------------------------------------------------------------------
# STEP 2: GROUND_TRUTH must list EVERY PII instance inside the first
# SCOPE_BLOCKS text blocks (paragraphs + table cells, in document order)
# -- not a curated sample of interesting examples. If you add or remove
# items from GROUND_TRUTH without re-checking against the actual blocks
# in that range, your precision number will be wrong again for the same
# reason the original evaluate.py was wrong.
# ----------------------------------------------------------------------
SCOPE_BLOCKS = 300 # <-- set this to match how far your labeling actually went

GROUND_TRUTH = [
    "Sarthak Malvadkar", "Kushal Subbayya Hegde", "Pushpa Kushal Hegde",
    "Rajesh Kushal Hegde", "Rohit Kushal Hegde", "Rakhi Girija Shetty", "Sandesh Bhagwat",
    "Amod Joshi", "Lokesh Shah", "Soumavo Sarkar", "Shanti Gopalkrishnan", "Kishan Rastogi",
    "Abhijit Diwan", "Lalit Muljibhai Sarvaiya",

    "cs.connect@kshinternational.com","ksh.ipo@nuvama.com","customerservice.mb@nuvama.com",
    "ksh@icicisecurities.com" ,"kshinternational.ipo@in.mpms.mufg.com",

    "+ 91 20 4505 3237","+91 22 4009 4400" ,"+91 22 6807 7100" ,"+91 81081 14949",

    "KSH International Limited ","Nuvama Wealth Management Limited ","ICICI Securities Limited",
    "MUFG Intime India Private Limited" ,"Waterloo Industrial Park VI Private Limited",
    "CARE Analytics and Advisory Private Limited", "Bhandary Metal Extrusion Private Limited",
    "KSH International Private Limited"
    
    "11/3, 11/4 and 11/5, Village Birdewadi, Chakan Taluka - Khed, Pune -- 410 501, Maharashtra, India",
    "201, Tower 2, Montreal Business Centre, Off Pallod Farms, Baner, Pune -- 411 045, Maharashtra, India"
]

# ----------------------------------------------------------------------
# STEP 3: run the pipeline, then evaluate against the scoped ground truth
# ----------------------------------------------------------------------
processor = DocxProcessor()
processor.process(input_path=INPUT_FILE, output_path=OUTPUT_FILE)

metrics = AutomatedEvaluator.evaluate(
    input_path=INPUT_FILE,
    output_path=OUTPUT_FILE,
    detector=processor.detector,       # reuse the already-loaded spaCy model
    ground_truth=GROUND_TRUTH,
    scope_blocks=SCOPE_BLOCKS,
)

print("\n" + "=" * 50)
print("AUTOMATED EVALUATION REPORT")
print("=" * 50)
for metric, value in metrics.items():
    print(f"{metric:<35}: {value}")