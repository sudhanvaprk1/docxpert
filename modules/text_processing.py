import re, os
from cleantext import clean
from modules.utils import chunk_text
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from app.config import Config 
import pymupdf4llm
config = Config()

# Custom function to extract text while handling multiple columns and noise
def extract_text_from_pdf(pdf):
    extracted_text = []
    
    for page in pdf.pages:
        # Handle multi-column PDFs by extracting words in order
        words = page.extract_words(use_text_flow=True)
        page_text = " ".join(word["text"] for word in words)

        # Remove headers/footers based on heuristics (e.g., first & last lines)
        lines = page_text.split("\n")
        if len(lines) > 2:  # Avoid removing small pages
            lines = lines[1:-1]  # Remove first & last lines (heuristic)
        
        extracted_text.append(" ".join(lines))

    return " ".join(extracted_text)

# Preprocess extracted text
def preprocess_text(text):
    text = clean(
        text,
        fix_unicode=True,
        to_ascii=True,
        lower=True,
        no_urls=True,
        no_emails=True,
        no_phone_numbers=True,
        no_numbers=False,
        no_punct=False,
    )
    
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text)
    cleaned_tokens = [word for word in tokens if word not in stop_words]

    return " ".join(cleaned_tokens)

# Process multiple PDFs
# def process_pdfs(pdf_paths):
#     all_chunks = []
#     for pdf_path in pdf_paths:
#         print(f"Processing PDF: {pdf_path}")
        
#         if pdf_path and os.path.exists(pdf_path):
#             with pdfplumber.open(pdf_path) as pdf:
#                 text = extract_text_from_pdf(pdf)
#                 cleaned_text = preprocess_text(text)
                
#                 # Chunk the cleaned text
#                 chunks = chunk_text(cleaned_text, chunk_size=config.CHUNK_SIZE, overlap=config.OVERLAP)
#                 all_chunks.extend(chunks)
    
#     return all_chunks

def process_pdfs(pdf_paths):
    all_chunks = []
    for pdf_path in pdf_paths:
        if pdf_path and os.path.exists(pdf_path):
            print(f"Processing PDF: {pdf_path}")
            md_text = pymupdf4llm.to_markdown(pdf_path)
            cleaned_text = preprocess_text(md_text)
            chunks = chunk_text(cleaned_text, chunk_size=config.CHUNK_SIZE, overlap=config.OVERLAP)
            all_chunks.extend(chunks)
    return all_chunks
