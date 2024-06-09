import os
from transformers import BertTokenizer, BertModel
from langchain_openai import ChatOpenAI
from langchain.schema import Document as LangchainDocument, HumanMessage
from typing import List

# Initialize OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Function to generate multiple prompts
def generate_prompts(user_prompt, relevant_contexts: List[LangchainDocument], openai_api_key: str):
    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model_name="gpt-3.5-turbo",
        temperature=0.7
    )
    
    # Combine the user prompt and relevant contexts
    combined_context = "\n".join([doc.page_content for doc in relevant_contexts])
    complete_input = f"Context:\n{combined_context}\n\nUser Input:\n{user_prompt}"
    
    # Define the instruction to guide the LLM
    instruction = f"""
    This is a prompt generation tool designed to assist users in creating effective prompts for AI-powered tasks.

    User Input:
    "The user has provided the following input through the UI: {user_prompt}."

    Expected Outcome:
    "The desired outcome is to generate several high-quality prompts based on the user's input and rank them based on their potential effectiveness for various AI models (including GPT-4) to achieve the user's goals."

    Instruction:
    1. Following the user's input, generate at least five prompts that could be used to achieve the user's desired outcome when used with different AI models.
    2. While generating prompts, prioritize clarity, conciseness, and focus. Ensure the prompts capture the essence of the user's input and guide the AI model towards a relevant and comprehensive response.
    3. Consider incorporating different prompt styles and techniques (e.g., question-based prompts, instruction-based prompts, exemplar prompts) to cater to the strengths of various AI models.
    4. After generating multiple prompts, employ a ranking mechanism to identify the single best prompt based on its clarity, potential effectiveness for different AI models, and alignment with the user's input.
    
    Output:
    "Provide the ranked list of prompts, with the highest-ranked prompt at the top. This prompt should be the one deemed most versatile and effective across various AI models for achieving the user's goals."
    """
    
    # Combine instruction and input for GPT-3.5-turbo
    complete_input_with_instruction = f"{instruction}\n\n{complete_input}"
    
    # Create the HumanMessage object for the prompt
    human_message = HumanMessage(content=complete_input_with_instruction)
    
    # Generate multiple prompts using GPT-3.5-turbo
    responses = [llm.invoke([human_message]) for _ in range(5)]
    
    # Extract prompts from responses
    prompts = [response.content for response in responses]
    
    return prompts

# Example usage (assuming relevant contexts and API key are provided)
if __name__ == "__main__":
    user_prompt = "What are week 3 challenge deliverables?"
    relevant_contexts = [LangchainDocument(page_content="Example context")]

    prompts = generate_prompts(user_prompt, relevant_contexts, openai_api_key)
    print("Generated Prompts:", prompts)


