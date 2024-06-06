import os
import json
from docx import Document as DocxDocument

def extract_text_from_docx(docx_folder):
    documents = []
    for docx_file in os.listdir(docx_folder):
        if docx_file.endswith(".docx"):
            docx_path = os.path.join(docx_folder, docx_file)
            doc = DocxDocument(docx_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            documents.append({"file_name": docx_file, "text": text})
    return documents

def save_extracted_texts(docx_folder, output_file):
    extracted_documents = extract_text_from_docx(docx_folder)
    with open(output_file, 'w') as file:
        json.dump(extracted_documents, file, indent=4)
    print(f"Extracted texts saved to {output_file}")

if __name__ == "__main__":
    docx_folder = "/home/moraa/Documents/10_academy/Week-7/documents"  # Adjust this path as needed
    output_file = "extracted_texts.json"
    save_extracted_texts(docx_folder, output_file)
