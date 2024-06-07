import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec, Index
from langchain_openai import OpenAIEmbeddings

# Load environment variables from .env file
load_dotenv()

# Initialize Pinecone
pinecone_api_key = os.getenv('PINECONE_API_KEY')

pc = Pinecone(api_key=pinecone_api_key)

# Check if the index exists; if not, create it
index_name = "wk7-prompt-tuning"
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

# Get the index info
index_info = pc.describe_index(index_name)
print("Index Info:", index_info)  # Print the full index info for debugging

# Extract the index host
index_host = index_info.get("host")
if not index_host:
    raise ValueError("Host information not found in the index description")

# Connecting to the index
index = Index(index_name, host=index_host)

# Initialize OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize the embeddings model
embed = OpenAIEmbeddings(
    model='text-embedding-ada-002',
    openai_api_key=openai_api_key
)

# Function to query Pinecone for relevant documents
def query_pinecone(prompt, embed_model, top_k=5):
    # Embed the user prompt
    prompt_embedding = embed_model.embed_query(prompt)
    
    # Query Pinecone
    result = index.query(vector=prompt_embedding, top_k=top_k, include_metadata=True, metric="cosine")
    
    # Extract the relevant chunks
    contexts = [match['metadata']['page_content'] for match in result['matches']]
    return contexts

# Main program
if __name__ == "__main__":
    # Get user prompt
    prompt = input("Enter your prompt: ")
    
    # Query Pinecone for relevant documents
    relevant_contexts = query_pinecone(prompt, embed)
    
    # Print the retrieved contexts
    for context in relevant_contexts:
        print(context)


