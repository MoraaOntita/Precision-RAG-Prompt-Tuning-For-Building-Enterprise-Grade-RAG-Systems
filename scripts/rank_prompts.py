import torch
import os
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List

# Initialize BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Function to rank prompts based on cosine similarity to user input
def rank_prompts(user_prompt, prompts: List[str]):
    # Encode the user input
    user_input_encoding = tokenizer(user_prompt, return_tensors='pt')
    user_input_output = model(**user_input_encoding)
    user_input_vector = user_input_output.last_hidden_state.mean(dim=1).detach().numpy()
    
    # Extract and encode prompts using BERT
    prompt_encodings = []
    for prompt in prompts:
        inputs = tokenizer(prompt, return_tensors='pt')
        outputs = model(**inputs)
        prompt_encodings.append(outputs.last_hidden_state.mean(dim=1).detach().numpy())

    # Calculate cosine similarity between user input and generated prompts
    similarities = [cosine_similarity(user_input_vector, prompt_vec)[0][0] for prompt_vec in prompt_encodings]
    
    # Rank the prompts based on similarity scores
    ranked_prompts = sorted(zip(prompts, similarities), key=lambda x: x[1], reverse=True)
    best_prompt = ranked_prompts[0][0]
    
    return best_prompt, [prompt for prompt, score in ranked_prompts]

# Example usage (assuming prompts are generated)
if __name__ == "__main__":
    user_prompt = "What are week 3 challenge deliverables?"
    prompts = [
        "Prompt 1 based on the user's input",
        "Prompt 2 based on the user's input",
        "Prompt 3 based on the user's input",
        "Prompt 4 based on the user's input",
        "Prompt 5 based on the user's input"
    ]

    best_prompt, ranked_prompts = rank_prompts(user_prompt, prompts)
    print("Best Prompt:", best_prompt)
    print("Ranked Prompts:", ranked_prompts)

