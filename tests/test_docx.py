from src.docx_processor import DocxProcessor

processor = DocxProcessor()

processor.process(
    input_path="data/input/Red Herring Prospectus.docx",
    output_path="data/output/Red Herring Prospectus_Redacted.docx",
)