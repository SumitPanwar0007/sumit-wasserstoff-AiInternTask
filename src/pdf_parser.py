from PyPDF2 import PdfReader
import os
import re
import logging
from .summarizer import summarize_text
from .keyword_extractor import extract_keywords
from .pdf_to_text import extract_text_from_pdf
from .text_cleaning import clean_text
from concurrent.futures import ThreadPoolExecutor, as_completed
from sklearn.feature_extraction.text import TfidfVectorizer



def process_pdf_for_summary_and_keywords(pdf_path, num_sentences=5, top_n=10):
    """Process a single PDF for summarization and keyword extraction."""
    pdf_text = extract_text_from_pdf(pdf_path)

     # Check if the extracted text is valid before proceeding
    if not pdf_text:  # If no text was extracted, return an error message
        logging.error(f"Failed to extract text from {pdf_path}")
        return None, None
    
    cleaned_text = clean_text(pdf_text)
    

    if not cleaned_text:
        logging.error(f"Cleand text is empty for {pdf_path}")
        return None, None
    summary = summarize_text(cleaned_text, num_sentences)
 
    
    keywords = extract_keywords(cleaned_text, top_n)
    
    return summary, keywords


def process_multiple_pdfs_for_summary_and_keywords(folder_path, max_workers=4):
    """Process multiple PDFs in parallel for summarization and keyword extraction."""
    pdf_summaries_keywords = {}

    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_pdf = {}
        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder_path, pdf_file)
            future = executor.submit(process_pdf_for_summary_and_keywords, pdf_path)
            future_to_pdf[future] = pdf_file

        for future in as_completed(future_to_pdf):
            pdf_name = future_to_pdf[future]
            try:
                summary, keywords = future.result()
                if summary is None and keywords is None:
                    pdf_summaries_keywords[pdf_name] = {"error": "Failed to extract text"}
                else:
                    pdf_summaries_keywords[pdf_name] = {
                        "summary": summary,
                        "keywords": keywords
                    }
            except Exception as e:
                pdf_summaries_keywords[pdf_name] = {
                    "error": str(e)
                }

    return pdf_summaries_keywords
