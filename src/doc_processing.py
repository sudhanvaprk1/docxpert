import pdfplumber
import re
from cleantext import clean
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Helper functions
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
    text = re.sub(r"\s+", " ", text).strip()
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text)
    cleaned_tokens = [word for word in tokens if word not in stop_words]
    return " ".join(cleaned_tokens)

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
