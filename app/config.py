from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    DOCUMENTS_DIR = "documents/raw_pdfs"
    EMBEDDINGS_DIR = "documents/embeddings"
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    FAISS_INDEX_PATH = "artifacts/faiss_index"
    CHUNK_SIZE = 500
    OVERLAP = 50
    LLAMA_MODEL_PATH = "meta-llama/Llama-3.2-1B"
    ARXIV_URL = "http://export.arxiv.org/api/query?"
    PUBMED_PMC_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    LLAMA_API_KEY = os.getenv("HF_TOKEN")
    INDEX_METADATA_PATH = "artifacts/index_metadata.json"
