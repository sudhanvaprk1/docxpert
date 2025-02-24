from dotenv import load_dotenv
import os

# Fetching Hugginface secret token
load_dotenv()
LLAMA_API_KEY = os.getenv("HF_TOKEN")
FAISS_INDEX_PATH = "artifacts/faiss_index"
INDEX_METADATA_PATH = "artifacts/index_metadata.json"
LLAMA_MODEL_NAME = "meta-llama/Llama-3.2-1B" 

# URLs
ARXIV_URL = "http://export.arxiv.org/api/query?"
PUBMED_PMC_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"