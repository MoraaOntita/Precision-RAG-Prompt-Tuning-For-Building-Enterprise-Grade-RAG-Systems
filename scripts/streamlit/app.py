import json
import os
import streamlit as st
from docx import Document
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import Document as LangchainDocument  

# Add the parent directory of 'scripts' to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scripts.retriever import retrieve_relevant_context

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize OpenAI model for chatting
llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model_name="gpt-4",  # Ensure you have access to GPT-4
    temperature=0.0
)

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

# Retrieve relevant context and get response from GPT-4
if st.button("Retrieve Relevant Context and Generate Response"):
    if prompt:
        try:
            relevant_contexts = retrieve_relevant_context(prompt)
            combined_context = "\n".join([doc.page_content for doc in relevant_contexts])
            combined_input = f"{combined_context}\n\nUser Prompt: {prompt}"

            # Generate response from GPT-4
            response = llm(combined_input)
            st.subheader("Generated Response")
            st.text_area("Response", response)
        except Exception as e:
            st.error(f"Error retrieving relevant context or generating response: {e}")
    else:
        st.error("Please enter a prompt to retrieve relevant context and generate a response.")
