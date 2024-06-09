import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

def generate_prompt(user_prompt, context):
    # Merge the user prompt with the retrieved context
    combined_prompt = f"Context: {context}\n\nUser Prompt: {user_prompt}"
    return combined_prompt

def get_gpt4_response(prompt):
    # Send the combined prompt to GPT-4 and get the response
    response = openai.Completion.create(
        model="text-davinci-003",  # Replace with the specific GPT-4 model name if available
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def generate_prompt_with_context(user_prompt, retrieved_contexts):
    # Combine all retrieved contexts into one string
    context_string = "\n\n".join([doc.page_content for doc in retrieved_contexts])
    
    # Generate the combined prompt
    combined_prompt = generate_prompt(user_prompt, context_string)
    
    # Get the response from GPT-4
    response = get_gpt4_response(combined_prompt)
    
    return response
