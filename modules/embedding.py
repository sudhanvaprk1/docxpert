import os
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
from app.config import Config

config = Config()

def create_faiss_index(chunks):
    model = SentenceTransformer(config.MODEL_NAME)
    embeddings = model.encode(chunks, convert_to_numpy=True)
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    # Map metadata to embeddings
    metadata = {i: chunks[i] for i in range(len(chunks))}
    return index, metadata

def query_faiss(faiss_index, query, metadata, top_k=5):
    model = SentenceTransformer(config.MODEL_NAME)
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = faiss_index.search(query_embedding, top_k)
    return [metadata[i] for i in indices[0]]
