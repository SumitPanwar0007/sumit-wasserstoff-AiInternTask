from PyPDF2 import PdfReader
import logging
def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using PyPDF2."""
    try:
        text=""
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            # text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:  # Only add non-empty text
                    text += page_text
                    
            if not text.strip():  # Check if no text was extracted
                logging.warning(f"No text extracted from {pdf_path}")
        # print("The text is: ",text)
        return text  # Return stripped text to avoid empty results
    except Exception as e:
        logging.error(f"Error reading {pdf_path}: {str(e)}")
        return ""