import streamlit as st
import json
import os
from docx import Document

# Function to extract text from docx files
def extract_text_from_docx(docx_folder):
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

# Extract documents (adjust the path to your data folder)
docx_folder = "./data"
extracted_documents = extract_text_from_docx(docx_folder)

# Streamlit UI
st.title("Prompt Generation Tool")

prompt_data = []

for doc in extracted_documents:
    st.subheader(f"Document: {doc['file_name']}")
    st.text_area("Document Content", doc['text'], height=200)

    prompt = st.text_input(f"Enter your prompt for {doc['file_name']}")
    expected_output = st.text_input(f"Enter the expected output for {doc['file_name']}")

    if st.button(f"Save Prompt for {doc['file_name']}"):
        prompt_data.append({
            "document": doc['file_name'],
            "prompt": prompt,
            "expected_output": expected_output
        })
        st.success(f"Prompt for {doc['file_name']} saved!")

# Save the prompt data to a JSON file
if st.button("Save All Prompts"):
    output_file = st.text_input("Enter the output filename", "prompts.json")
    if output_file:
        with open(output_file, 'w') as file:
            json.dump(prompt_data, file, indent=4)
        st.success(f"Prompt data saved to {output_file}")
