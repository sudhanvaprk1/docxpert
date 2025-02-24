from modules.utils import get_raw_doc_ids, fetch_and_save_data

def fetch_documents(subject):
    raw_doc_ids = get_raw_doc_ids()
    arxiv_data_paths = fetch_and_save_data(subject, raw_doc_ids, source='arxiv')
    pubmed_data_paths = fetch_and_save_data(subject, raw_doc_ids, source='pubmed')
    arxiv_data_paths.extend(pubmed_data_paths)
    return arxiv_data_paths
