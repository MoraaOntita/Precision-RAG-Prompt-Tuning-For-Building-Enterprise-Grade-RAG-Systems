# scripts/embed_texts.py

import os
import json
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set or is invalid.")

# Initialize the embeddings model
embed = OpenAIEmbeddings(
    model='text-embedding-ada-002',
    openai_api_key=openai_api_key
)

# Function to load chunked documents from a JSON file
def load_chunked_documents(input_file):
    with open(input_file, 'r') as file:
        doc_dicts = json.load(file)
    return [Document(page_content=doc['page_content'], metadata=doc['metadata']) for doc in doc_dicts]

# Function to save embeddings to a JSON file
def save_embeddings(embeddings, documents, output_file):
    data = []
    for emb, doc in zip(embeddings, documents):
        data.append({
            "embedding": emb,
            "metadata": doc.metadata
        })
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Embeddings saved to {output_file}")

if __name__ == "__main__":
    input_file = "chunked_documents.json"
    output_file = "embeddings.json"

    # Load the chunked documents
    chunked_documents = load_chunked_documents(input_file)

    # Create an array of text to embed
    context_array = [doc.page_content for doc in chunked_documents]

    # Generate embeddings for the documents
    emb_vectors = embed.embed_documents(context_array)

    # Save the embeddings
    save_embeddings(emb_vectors, chunked_documents, output_file)
