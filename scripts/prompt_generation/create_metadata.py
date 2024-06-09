from docx import Document
import os
import json

# Function to load documents from a folder (assuming they are in .docx format)
def load_documents(docx_folder):
    documents = []
    for docx_file in os.listdir(docx_folder):
        if docx_file.endswith(".docx"):
            docx_path = os.path.join(docx_folder, docx_file)
            doc = Document(docx_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            documents.append({"file_name": docx_file, "text": text})
    return documents

# Function to create metadata for the documents
def create_metadata(documents):
    metadata = []
    for doc in documents:
        metadata.append({"file_name": doc["file_name"]})
    return metadata

# Example usage
if __name__ == "__main__":
    # Adjust the path to your document folder
    docx_folder = "documents"  # Assuming documents are located in the same directory
    
    # Load documents from the folder
    documents = load_documents(docx_folder)
    
    # Create metadata for the documents
    metadata = create_metadata(documents)
    
    # Save metadata to a JSON file in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    metadata_file = os.path.join(script_dir, "metadata.json")
    with open(metadata_file, "w") as file:
        json.dump(metadata, file, indent=4)


