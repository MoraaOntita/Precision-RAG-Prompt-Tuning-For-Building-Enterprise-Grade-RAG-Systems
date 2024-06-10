# tests/test_prompt.py
import pytest
from scripts.prompt_testing_and_ranking.prompt import Prompt

def test_prompt_initialization():
    prompt_text = "Generate a summary for the business need section."
    prompt = Prompt(prompt_text)
    assert prompt.text == prompt_text
    assert prompt.elo_rating == 1000

def test_prompt_representation():
    prompt_text = "Generate a summary for the business need section."
    prompt = Prompt(prompt_text)
    assert repr(prompt) == f"Prompt({prompt_text[:30]}... ELO: {prompt.elo_rating})"
