# tests/test_retriever.py
import pytest
from scripts.prompt_generation.retriever import retrieve_relevant_context

def test_retrieve_relevant_context():
    prompt = "What is the main goal of the business need section?"
    context = retrieve_relevant_context(prompt)
    assert isinstance(context, list)
    assert len(context) > 0
