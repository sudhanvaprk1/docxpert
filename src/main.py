# Imports
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from transformers import pipeline, LlamaForCausalLM, LlamaTokenizer, AutoTokenizer, AutoModelForCausalLM
import nltk
import pickle
import pdfplumber
import re
from constants import LLAMA_API_KEY, LLAMA_MODEL_NAME, FAISS_INDEX_PATH, INDEX_METADATA_PATH
from arxiv_pubmed_functions import fetch_arxiv_data, fetch_pmc_data, save_arxiv_pdf, save_pmc_pdf_direct
from doc_processing import extract_text_from_pdf, preprocess_text, chunk_text

# Fetching stopwards and punkt modules of nltk
nltk.download("stopwords")
nltk.download("punkt")

# Load pre-trained embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load LLaMA model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(LLAMA_MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(LLAMA_MODEL_NAME, torch_dtype="auto")
qa_pipeline = pipeline("text-generation", model=LLAMA_MODEL_NAME, tokenizer=tokenizer)


def get_raw_doc_ids(doc_embeddings_folder="documents/raw_pdfs"):
    raw_doc_ids = []

    # Check if the folder exists
    if os.path.exists(doc_embeddings_folder) and os.path.isdir(doc_embeddings_folder):
        # Iterate over the files in the directory
        for file in os.listdir(doc_embeddings_folder):
            # Ensure we process only files (not directories) and extract the name without extension
            if os.path.isfile(os.path.join(doc_embeddings_folder, file)):
                file_name, _ = os.path.splitext(file)
                raw_doc_ids.append(file_name)
    else:
        print(f"Folder '{doc_embeddings_folder}' does not exist or is not a directory.")

    return raw_doc_ids

def fetch_and_save_data(subject, raw_doc_ids, source):
    if source == "arxiv":
        rel_ids = fetch_arxiv_data(subject, max_results=10)
        if rel_ids:
            for paper in rel_ids:
                if paper not in raw_doc_ids:
                    save_arxiv_pdf(paper)
    else:
        rel_ids = fetch_pmc_data(subject, max_results=10)
        if rel_ids:
            for paper in rel_ids:
                if paper not in raw_doc_ids:
                    save_pmc_pdf_direct(paper)

def embed_and_add_to_faiss(raw_doc_ids):
    extracted_doc_ids = get_raw_doc_ids(doc_embeddings_folder="documents/processed_pdfs")
    for raw_id in raw_doc_ids:
        if raw_id not in extracted_doc_ids:
            text = extract_text_from_pdf()
            cleaned_text = preprocess_text(text)
            chunks = chunk_text(cleaned_text)
            embeddings = embedding_model.encode(chunks)
            faiss_index.add(np.array(embeddings, dtype='float32'))

def main(query, subject, file=None):
    # Getting list of all the document ids that are already processed
    raw_doc_ids = get_raw_doc_ids()

    # Fetching all the documents from arXiv and pubmed pmc for the given subject and
    # Saving as PDFs
    fetch_and_save_data(subject, raw_doc_ids, source='arxiv')
    fetch_and_save_data(subject, raw_doc_ids, source='pubmed')

    # Processing PDFs

if __name__ == "__main__":
    main("xyz", "heart disease")
