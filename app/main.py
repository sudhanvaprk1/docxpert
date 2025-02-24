from flask import Flask, request, jsonify
from app.config import Config
from modules.data_fetch import fetch_documents
from modules.text_processing import process_pdfs
from modules.embedding import create_faiss_index, query_faiss
from modules.query_handler import generate_response
from diskcache import Cache

cache = Cache("./cache")

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/docxpert/query", methods=["POST"])
def query():
    data = request.get_json()
    query = data.get("query")
    subject = data.get("subject")
    print(f"Received query: {query} for subject: {subject}")
    if not query or not subject:
        return jsonify({"error": "Query and subject are required"}), 400

    # Creating a cache key 
    cache_key = f"{subject}_chunks"

    # Loading chunks from cache if the subject was processed in this session
    if cache_key in cache:
        chunks = cache[cache_key]
        print("Loaded chunks from cache")
    else:
        # Fetch documents
        pdf_paths = fetch_documents(subject)
        print(f"Documents fetched and saved")
        
        # Process PDFs (extract, clean, chunk)
        print(pdf_paths)
        chunks = process_pdfs(pdf_paths)
        print(f"Created chunks")

        # Cache processed chunks
        cache[cache_key] = chunks  
    
    # Creating a cache key for Faiss Index
    cache_key_faiss = f"{subject}_faiss"

    if cache_key_faiss in cache:
        faiss_index, metadata = cache[cache_key_faiss]
        top_chunks = query_faiss(faiss_index, query, metadata)
        print("Loaded FAISS index from cache")
    else:
        # Embed chunks and create/query FAISS index
        faiss_index, metadata = create_faiss_index(chunks)
        top_chunks = query_faiss(faiss_index, query, metadata)
        cache[cache_key_faiss] = (faiss_index, metadata)
        print(f"Fetched top chunks")

    # Generate response using the LLM
    response = generate_response(query, top_chunks)
    return jsonify({"response": response})
    

if __name__ == "__main__":
    app.run(debug=True)
