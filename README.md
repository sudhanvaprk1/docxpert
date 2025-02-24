# DocXpert - Smart Document Querying

DocXpert is an AI-powered document querying system that allows users to extract relevant information from documents efficiently. It leverages NLP techniques, FAISS for similarity search, and a Large Language Model (LLM) to generate responses based on extracted content.

## Features

- Fetches relevant documents based on subject
- Extracts, cleans, and chunks PDF content
- Embeds document chunks and creates a FAISS index
- Queries FAISS for relevant content
- Uses an LLM to generate responses
- Provides a user-friendly Streamlit interface

## Tech Stack

- **Backend**: Flask
- **Frontend**: Streamlit
- **PDF Processing**: pymupdf4llm, cleantext
- **Embeddings & Search**: FAISS, Hugging Face Sentence Transformers
- **ML & NLP**: Scikit-learn, NLTK, NumPy, Pandas

## Installation

Ensure you have Python 3.8+ installed. Clone the repository and install dependencies:

```sh
pip install -r requirements.txt
```

## Running the Application

Start the Flask backend:

```sh
python run.py
```

Start the Streamlit frontend:

```sh
streamlit run streamlit_app.py
```

## API Endpoints

### Query Documents

**Endpoint:** `POST /docxpert/query`

**Request Body:**

```json
{
  "query": "What is the difference between weak AI and strong AI?",
  "subject": "AI"
}
```

**Response:**

```json
{
  "response": "Weak AI focuses on specific tasks while strong AI possesses general intelligence."
}
```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

---

Happy Querying! 🚀

