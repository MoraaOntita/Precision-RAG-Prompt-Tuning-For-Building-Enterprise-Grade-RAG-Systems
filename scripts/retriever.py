import os
from dotenv import load_dotenv
import pinecone
#  from langchain.vectorstores import Pinecone as PineconeVectorStore
from langchain_community.vectorstores import Pinecone
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize Pinecone API key
pinecone_api_key = os.getenv('PINECONE_API_KEY')
if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY environment variable is not set.")

# Initialize the client connection
pinecone_api_key = os.environ.get('PINECONE_API_KEY')

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
    
# Connecting
index = pc.Index(index_name)

# Initialize the embeddings model
embeddings = OpenAIEmbeddings(
    model='text-embedding-ada-002',
    openai_api_key=openai_api_key
)

def retrieve_relevant_context(prompt, top_k=5):
    # Generate embedding for the prompt
    prompt_embedding = embeddings.embed_query(prompt)
    
    # Query Pinecone for the most relevant documents
    results = index.query(queries=[prompt_embedding], top_k=top_k, include_metadata=True)
    
    # Extract and return the relevant documents
    relevant_documents = [
        Document(page_content=result['metadata']['text'], metadata=result['metadata'])
        for result in results['matches']
    ]
    return relevant_documents

