import streamlit as st
import requests
import json

def query_backend(query, subject):
    url = "http://127.0.0.1:5000/docxpert/query" 
    payload = {"query": query, "subject": subject}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return response.json().get("response", "No response received.")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit UI
st.set_page_config(page_title="DocXpert", page_icon="📄", layout="centered")
st.title("📄 DocXpert - Smart Document Querying")

st.markdown(
    """
    **DocXpert** helps you extract relevant information from documents efficiently.
    Enter your query and subject below, and let AI do the rest! 🚀
    """,
    unsafe_allow_html=True,
)

# Input fields
query = st.text_area("🔍 Enter your query:", height=100)
subject = st.text_input("📂 Enter subject name:")

if st.button("Submit Query", use_container_width=True):
    if query.strip() and subject.strip():
        with st.spinner("Processing your request..."):
            response = query_backend(query, subject)
        st.success("✅ Response received!")
        st.text_area("📜 AI Response:", value=response, height=200)
    else:
        st.warning("⚠️ Please enter both a query and subject.")

# Footer
st.markdown("---")
st.markdown("👨‍💻 Developed with ❤️ using Streamlit")
