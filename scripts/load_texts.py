# scripts/load_texts.py

import json
from langchain.schema import Document
from langchain.document_loaders.base import BaseLoader

class RawTextLoader(BaseLoader):
    def __init__(self, text, metadata=None):
        self.text = text
        self.metadata = metadata or {}

    def load(self):
        return [Document(page_content=self.text, metadata=self.metadata)]

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

if __name__ == "__main__":
    input_file = "extracted_texts.json"
    extracted_documents = load_extracted_texts(input_file)
    documents = create_langchain_documents(extracted_documents)
    print(f"Loaded {len(documents)} documents into LangChain.")
