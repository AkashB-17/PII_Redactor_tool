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
            
            # Find and redact the original text, replacing with fake text
            for original_text, fake_text in mapping.items():
                # Search for the exact coordinates of the PII on the page
                text_instances = page.search_for(original_text)
                
                for inst in text_instances:
                    # Add redaction annotation (blocks out the original text)
                    page.add_redact_annot(inst, fill=(0, 0, 0)) # Black box
                    
                    # Insert the fake text slightly above the bottom-left of the bounding box
                    page.insert_text((inst.x0, inst.y1 - 2), fake_text, fontsize=10, color=(1, 1, 1)) 
            
            # Apply all redactions to the page
            page.apply_redactions()

        # Save the new PDF
        doc.save(output_path)
        print(f"Saved redacted PDF -> {output_path}")