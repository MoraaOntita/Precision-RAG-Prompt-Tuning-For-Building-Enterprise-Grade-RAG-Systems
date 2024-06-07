import os
import json
from dotenv import load_dotenv
import pinecone
from pinecone import Pinecone, Index
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document

# Load environment variables from .env file
load_dotenv()

# Initialize Pinecone
pinecone_api_key = os.getenv('PINECONE_API_KEY')
pinecone_env = os.getenv('PINECONE_ENV')

pc = Pinecone(api_key=pinecone_api_key, environment=pinecone_env)

# Connect to the index
index_name = "wk7-prompt-tuning"
index = Index(index_name, host=pc.project_name)

# Initialize OpenAI API key (replace 'your-openai-api-key' with your actual API key)
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
    result = index.query(vector=prompt_embedding, top_k=top_k, include_metadata=True)
    
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

