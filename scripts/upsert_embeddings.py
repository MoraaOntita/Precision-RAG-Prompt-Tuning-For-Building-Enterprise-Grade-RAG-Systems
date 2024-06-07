# scripts/upsert_embeddings.py

import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load environment variables from .env file
load_dotenv()

# Initialize Pinecone API key
pinecone_api_key = os.getenv('PINECONE_API_KEY')
if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY environment variable is not set.")

# Initialize the Pinecone client
pc = Pinecone(api_key=pinecone_api_key)

index_name = "wk7-prompt-tuning"

# Check if the index exists; if not, create it
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-east-1'
        )
    )

# Connecting to the index
index = pc.Index(index_name)

# Function to load embeddings from a JSON file
def load_embeddings(input_file):
    with open(input_file, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    input_file = "embeddings.json"

    # Load the embeddings
    embeddings_data = load_embeddings(input_file)

    # Upsert the embeddings into Pinecone
    for item in embeddings_data:
        emb = item['embedding']
        metadata = item['metadata']
        metadata['id'] = f"{metadata['source']}_{metadata['chunk_index']}"

        # Upsert the embedding into Pinecone
        index.upsert([(metadata['id'], emb, metadata)])

    # Query Pinecone to ensure the data is stored
    print(index.describe_index_stats())