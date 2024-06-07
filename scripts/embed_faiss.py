import os
import faiss
import json
import numpy as np  # Import numpy for array operations
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

if __name__ == "__main__":
    input_file = "chunked_documents.json"
    
    # Load the chunked documents
    chunked_documents = load_chunked_documents(input_file)

    # Create an array of text to embed
    context_array = [doc.page_content for doc in chunked_documents]

    # Generate embeddings for the documents
    emb_vectors_list = embed.embed_documents(context_array)
    emb_vectors = np.array(emb_vectors_list)  # Convert list to numpy array

    # Initialize a FAISS index
    dimension = emb_vectors.shape[1]  # Dimensionality of your vectors
    index = faiss.IndexFlatL2(dimension)  # Use L2 distance for similarity search

    # Add vectors to the index
    index.add(emb_vectors)

    # Save the FAISS index
    faiss.write_index(index, "faiss_index.index")

    print("FAISS index created and saved successfully.")

