"""
PDF Processor

Extracts text from PDF, detects PII, redacts the original 
text blocks, and overlays fake synthetic data.
"""

import fitz  # PyMuPDF
from src.detector import PIIDetector
from src.anonymizer import PIIAnonymizer

class PdfProcessor:
    def __init__(self):
        self.detector = PIIDetector()
        self.anonymizer = PIIAnonymizer()

    def process(self, input_path: str, output_path: str):
        # Open the PDF
        doc = fitz.open(input_path)
        
        for page in doc:
            # Extract text from the page
            text = page.get_text("text")
            if not text or not text.strip():
                continue
            
            # Detect PII
            entities = self.detector.detect(text)
            if not entities:
                continue
                
            # Generate mappings
            mapping = self.anonymizer.build_mapping(entities)

            # Step 1: mark every PII instance for redaction, but don't draw
            # the replacement text yet -- apply_redactions() strips ALL
            # content inside a marked rectangle, including anything drawn
            # there before it runs. Collect (rect, fake_text) pairs instead.
            pending_overlays = []
            for original_text, fake_text in mapping.items():
                text_instances = page.search_for(original_text)
                for inst in text_instances:
                    page.add_redact_annot(inst, fill=(0, 0, 0))  # black box
                    pending_overlays.append((inst, fake_text))

            # Step 2: actually apply the redactions now -- this blanks out
            # the original PII and paints the black fill.
            page.apply_redactions()

            # Step 3: now that the boxes are blanked, draw the fake text
            # into them. Anything inserted after this point survives.
            for inst, fake_text in pending_overlays:
                page.insert_text((inst.x0, inst.y1 - 2), fake_text, fontsize=10, color=(1, 1, 1))

        # Save the new PDF
        doc.save(output_path)
        print(f"Saved redacted PDF -> {output_path}")