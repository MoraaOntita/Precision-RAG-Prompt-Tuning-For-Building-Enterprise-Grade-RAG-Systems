from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import os

# Function to create LangChain Document objects from a list of dictionaries
def create_documents(doc_dicts):
    return [Document(page_content=doc['page_content'], metadata=doc['metadata']) for doc in doc_dicts]

# Function to save LangChain Document objects to a JSON file
def save_documents(documents, output_file):
    doc_dicts = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in documents]
    with open(output_file, 'w') as file:
        json.dump(doc_dicts, file, indent=4)
    print(f"Chunked documents saved to {output_file}")

# Function to chunk documents using RecursiveCharacterTextSplitter
def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    chunked_documents = []
    for document in documents:
        chunks = text_splitter.split_text(document.page_content)
        for i, chunk in enumerate(chunks):
            chunk_metadata = document.metadata.copy()
            chunk_metadata["chunk_index"] = i
            chunked_documents.append(Document(page_content=chunk, metadata=chunk_metadata))
    return chunked_documents

if __name__ == "__main__":
    input_file = "loaded_documents.json"  # Adjust this as needed
    output_file = "chunked_documents.json"

    # Load the documents
    with open(input_file, 'r') as file:
        doc_dicts = json.load(file)
    
    documents = create_documents(doc_dicts)

    # Chunk the documents
    chunked_documents = chunk_documents(documents)

    # Save the chunked documents
    save_documents(chunked_documents, output_file)
