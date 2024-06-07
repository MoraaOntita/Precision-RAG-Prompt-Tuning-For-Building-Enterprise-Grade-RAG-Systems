# scripts/load_texts.py

import json
from llama_index.core import Document
from langchain.document_loaders.base import BaseLoader
from llama_index.core import VectorStoreIndex
import warnings

warnings.filterwarnings("ignore", message="Importing ChatMessageHistory from langchain.memory is deprecated")

class RawTextLoader(BaseLoader):
    def __init__(self, text, metadata=None):
        self.text = text
        self.metadata = metadata or {}

    def load(self):
        return [Document(text=self.text, metadata=self.metadata)]

def load_extracted_texts(input_file):
    with open(input_file, 'r') as file:
        extracted_documents = json.load(file)
    return extracted_documents

def create_langchain_documents(extracted_documents):
    loaders = [RawTextLoader(text=doc['text'], metadata={"source": doc['file_name']}) for doc in extracted_documents]
    documents = []
    for loader in loaders:
        documents.extend(loader.load())
    return documents

def save_documents(documents, output_file):
    doc_dicts = [{"text": doc.text, "metadata": doc.metadata} for doc in documents]
    with open(output_file, 'w') as file:
        json.dump(doc_dicts, file, indent=4)
    print(f"Loaded documents saved to {output_file}")

if __name__ == "__main__":
    input_file = "extracted_texts.json"
    output_file = "loaded_documents.json"

    extracted_documents = load_extracted_texts(input_file)
    documents = create_langchain_documents(extracted_documents)
    print(f"Loaded {len(documents)} documents into LangChain.")

    # Create the index from documents
    index = VectorStoreIndex.from_documents(documents)

    # Optionally, save the index to disk for persistence
    index.set_index_id("vector_index")
    index.storage_context.persist("./storage")

    # Save the documents
    save_documents(documents, output_file)
