import json
import os
import streamlit as st
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
docx_folder = "./documents"
extracted_documents = extract_text_from_docx(docx_folder)

# Streamlit UI
st.title("Prompt Generation Tool")

# Let user select a document
document_names = [doc['file_name'] for doc in extracted_documents]
selected_document_name = st.selectbox("Select a document", document_names)

# Find the selected document
selected_document = next(doc for doc in extracted_documents if doc['file_name'] == selected_document_name)

# Display selected document's content
st.subheader(f"Document: {selected_document['file_name']}")
st.text_area("Document Content", selected_document['text'], height=200)

# Prompt for user input
prompt = st.text_input(f"Enter your prompt for {selected_document['file_name']}")
expected_output = st.text_input(f"Enter the expected output for {selected_document['file_name']}")

# Container to store prompt data
if 'prompt_data' not in st.session_state:
    st.session_state.prompt_data = []

# Save prompt
if st.button(f"Save Prompt for {selected_document['file_name']}"):
    st.session_state.prompt_data.append({
        "document": selected_document['file_name'],
        "prompt": prompt,
        "expected_output": expected_output
    })
    st.success(f"Prompt for {selected_document['file_name']} saved!")

# Save all prompt data to a JSON file
if st.button("Save All Prompts"):
    output_file = st.text_input("Enter the output filename", "prompts.json")
    if output_file:
        with open(output_file, 'w') as file:
            json.dump(st.session_state.prompt_data, file, indent=4)
        st.success(f"Prompt data saved to {output_file}")


