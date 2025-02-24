import requests
import xml.etree.ElementTree as ET
from constants import ARXIV_URL, PUBMED_PMC_URL
import requests
from bs4 import BeautifulSoup



def fetch_arxiv_data(query, max_results=10):
    params = {
        'search_query': query,
        'start': 0,
        'max_results': max_results
    }
    response = requests.get(ARXIV_URL, params=params)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        data = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
            link = entry.find('{http://www.w3.org/2005/Atom}id').text
            paper_id = link.split('/')[-1]
            data.append({'id': paper_id, 'title': title, 'summary': summary, 'link': link})
        return data
    else:
        raise Exception(f"Failed to fetch data from arXiv: {response.status_code}")

def fetch_pmc_data(query, max_results=10):
    """
    Fetch PMC (PubMed Central) IDs for articles matching a query.
    
    Args:
    query (str): The search query.
    max_results (int): The maximum number of results to fetch.
    
    Returns:
    list: A list of PMC IDs.
    """
    params = {
        'db': 'pmc',  # Query the PMC database
        'term': query,
        'retmax': max_results,
        'retmode': 'json'
    }
    response = requests.get(PUBMED_PMC_URL, params=params)
    if response.status_code == 200:
        result = response.json()
        ids = result.get('esearchresult', {}).get('idlist', [])
        pmc_ids = [f"PMC{id}" for id in ids]
        return pmc_ids
    else:
        raise Exception(f"Failed to fetch data from PMC: {response.status_code}")
    
def save_arxiv_pdf(paper_id, save_dir_path="documents/raw_pdfs/"):
    """
    Save an arXiv paper as a PDF file.
    
    Args:
    paper_id (str): arXiv paper ID.
    save_path (str): Path to save the downloaded PDF.
    """
    pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(save_dir_path + f"{paper_id}.pdf", 'wb') as f:
            f.write(response.content)
        print(f"Saved the PDF for {paper_id}")
    else:
        print(f"Failed to download {paper_id}: {response.status_code}")

def fetch_pmc_pdf_url(pmcid):
    """
    Fetch the PDF URL for a PMC article using its PMCID.
    
    Args:
    pmcid (str): PubMed Central ID.
    
    Returns:
    str: URL of the PDF if found, None otherwise.
    """
    base_url = f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(base_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Locate the PDF link
        pdf_link = soup.find('a', href=lambda href: href and 'pdf' in href.lower())
        if pdf_link:
            return "https://pmc.ncbi.nlm.nih.gov/" + pdf_link['href']
        else:
            print(f"No PDF link found for PMCID {pmcid}")
    else:
        print(f"Failed to fetch page for PMCID {pmcid}: {response.status_code}")
    
    return None

def save_pmc_pdf_direct(pmcid, save_dir_path):
    """
    Save a PMC paper as a PDF file by constructing the URL.
    
    Args:
    pmcid (str): PubMed Central ID (e.g., "PMC11295910").
    pdf_name (str): PDF filename (e.g., "gh-19-1-1342.pdf").
    save_path (str): Path to save the downloaded PDF.
    """
    # Construct the PDF URL
    pdf_url = f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/pdf/"
    print(f"Downloading PDF from: {pdf_url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(pdf_url, headers=headers)
    
    if response.status_code == 200:
        with open(save_dir_path + f"{pmcid}.pdf", 'wb') as f:
            f.write(response.content)
        print(f"PDF saved successfully: {pmcid}")
    else:
        print(f"Failed to download PDF: HTTP {response.status_code}")