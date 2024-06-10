import json
import os
import streamlit as st
from docx import Document
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import Document as LangchainDocument
import logging

# Add the parent directory of 'scripts' to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scripts.prompt_generation.retriever import retrieve_relevant_context
from scripts.prompt_generation.prompt_generator import generate_prompts
from scripts.prompt_testing_and_ranking.prompt import Prompt
from scripts.prompt_testing_and_ranking.monte_carlo import monte_carlo_matchmaking
from scripts.prompt_testing_and_ranking.elo_rating import update_elo

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

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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

# New functionality: Retrieve relevant context and get response from GPT-4
if st.button("Generate and Rank Prompts"):
    if prompt:
        try:
            # Retrieve relevant contexts from Pinecone
            retrieved_contexts = retrieve_relevant_context(prompt)
            best_prompt, ranked_prompts = generate_prompts(prompt, retrieved_contexts, openai_api_key)
            
            # Display the best prompt
            st.subheader("Best Generated Prompt")
            st.text_area("Best Prompt", best_prompt)
            
            # Display all ranked prompts
            st.subheader("All Ranked Prompts")
            for i, ranked_prompt in enumerate(ranked_prompts):
                st.text_area(f"Ranked Prompt {i+1}", ranked_prompt)
        except Exception as e:
            st.error(f"Error generating and ranking prompts: {e}")
            logging.error(f"Error generating and ranking prompts: {e}")
    else:
        st.error("Please enter a prompt to retrieve relevant context and generate a response.")

# Function to evaluate and rank prompts using Monte Carlo and ELO rating
if st.button("Evaluate and Rank Prompts"):
    try:
        # Initialize prompts
        prompt_objects = [Prompt(text=p['prompt']) for p in st.session_state.prompt_data]

        # Run Monte Carlo matchmaking
        monte_carlo_matchmaking(prompt_objects, num_simulations=100)

        # Display ranked prompts
        ranked_prompts = sorted(prompt_objects, key=lambda x: x.elo_rating, reverse=True)
        st.subheader("Ranked Prompts")
        for i, prompt_obj in enumerate(ranked_prompts):
            st.text_area(f"Ranked Prompt {i+1} (ELO: {prompt_obj.elo_rating})", prompt_obj.text)
    except Exception as e:
        st.error(f"Error evaluating and ranking prompts: {e}")
        logging.error(f"Error evaluating and ranking prompts: {e}")
