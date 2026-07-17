"""
Automated PII Evaluator

Diffs the input and output documents to find what was successfully redacted,
checks the anonymizer mapping for over-redaction, and calculates metrics.
"""

from docx import Document

class AutomatedEvaluator:

    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extracts text from both paragraphs and tables in a DOCX."""
        doc = Document(file_path)
        text_blocks = []
        
        # Extract paragraph text
        for p in doc.paragraphs:
            if p.text.strip():
                text_blocks.append(p.text.strip())
                
        # Extract table text
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        if p.text.strip():
                            text_blocks.append(p.text.strip())
                            
        return " ".join(text_blocks)

    @staticmethod
    def evaluate(input_path: str, output_path: str, actual_replacements: dict, ground_truth: list) -> dict:
        """
        Compares the input file, output file, and replacement mapping 
        against the ground truth to calculate ML metrics.
        """
        original_text = AutomatedEvaluator.extract_text_from_docx(input_path)
        redacted_text = AutomatedEvaluator.extract_text_from_docx(output_path)
        
        tp, fp, fn = 0, 0, 0
        
        # 1. Calculate True Positives & False Negatives (Diffing the files)
        for entity in ground_truth:
            # If it was in the original but is missing from the output, it was successfully redacted
            if entity in original_text and entity not in redacted_text:
                tp += 1
            # If it is STILL in the redacted output, the detector missed it
            elif entity in original_text and entity in redacted_text:
                fn += 1
                
        # 2. Calculate False Positives (Analyzing the mapping log)
        # If the script replaced a string that isn't in our ground truth, it over-redacted.
        for replaced_string in actual_replacements.keys():
            if replaced_string not in ground_truth:
                fp += 1

        # 3. Calculate Metrics
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        return {
            "True Positives": tp,
            "False Positives": fp,
            "False Negatives": fn,
            "Precision": round(precision, 4),
            "Recall": round(recall, 4),
            "F1-Score": round(f1_score, 4)
        }