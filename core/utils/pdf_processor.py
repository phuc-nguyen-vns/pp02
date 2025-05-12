import os, sys
from pathlib import Path
sys.path.append(Path(os.getcwd(),"PP02").as_posix())
from core.embedders.embedder_2 import embedding
from core.clients.meilisearch import MeiliClient as client
from api_configs import configs


# Function to setup MeiliSearch index
def setup_meilisearch_index(index_name='documents'):
    try:
        # Check if index exists
        client.get_index(index_name)
        print(f"Index '{index_name}' already exists")
    except:
        # Create the index if it doesn't exist
        print(f"Creating index '{index_name}'...")
        client.create_index(index_name, {'primaryKey': 'id'})
    # Configure the index with settings that your MeiliSearch version supports
    print(f"Updating settings for index '{index_name}'...")

    client.index(index_name).update_settings(configs.meili_index_settings)
    
    return index_name


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            pages_text = []
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                pages_text.append(text)
                
            return pages_text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {str(e)}")
        return []


# Function to create chunks using tiktoken
def create_chunks(text, max_tokens=512, overlap_percentage=0.2):
    tokens = encoding.encode(text)
    overlap_tokens = int(max_tokens * overlap_percentage)
    
    chunks = []
    i = 0
    
    while i < len(tokens):
        # Get chunk tokens
        chunk_end = min(i + max_tokens, len(tokens))
        chunk_tokens = tokens[i:chunk_end]
        
        # Decode back to text
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
        
        # Move to next chunk with overlap
        i += max_tokens - overlap_tokens
        
        # If we're at the end of the document, break
        if i >= len(tokens):
            break
    
    return chunks


# Function to process a single PDF file and create chunks with embeddings
def process_single_pdf(pdf_path):
    # Get just the filename from the path
    pdf_file = os.path.basename(pdf_path)
    
    all_documents = []
    
    # Extract text from each page
    pages_text = extract_text_from_pdf(pdf_path)
    
    print(f"==> Extracted text from {len(pages_text)} pages in {pdf_file}")
    
    for page_num, page_text in enumerate(tqdm(pages_text, desc=f"Processing pages in {pdf_file}")):
        # Create chunks for this page
        chunks = create_chunks(page_text)
        
        print(f"==> Created {len(chunks)} chunks for page {page_num+1}")
        
        for chunk_num, chunk_text in enumerate(chunks):
            # Generate embedding for this chunk
            embedding = embedding(chunk_text)
            
            # Create document with metadata and embedding
            document = {
                'id': str(uuid4()),
                'filename': pdf_file,
                'page': page_num + 1,
                'chunk': chunk_num + 1,
                'content': chunk_text,
                'total_pages': len(pages_text),
                'total_chunks_in_page': len(chunks),
                '_vectors': {"embedder": embedding}  # Store the embedding as a regular field
            }
            
            all_documents.append(document)
    
    return all_documents