import pytest
from scripts.prompt_generation.prompt_generator import generate_prompts

def test_generate_prompts():
    prompt = "Generate a summary for the business need section."
    contexts = ["The business need section outlines the main goals."]
    api_key = "test_api_key"
    best_prompt, ranked_prompts = generate_prompts(prompt, contexts, api_key)
    assert isinstance(best_prompt, str)
    assert isinstance(ranked_prompts, list)
    assert len(ranked_prompts) > 0
