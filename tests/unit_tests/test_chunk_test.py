# tests/test_chunk_test.py
import pytest
from scripts.prompt_generation import chunk_text

def test_chunk_text():
    text = "This is a simple text that needs to be chunked."
    chunk_size = 10
    chunks = chunk_text(text, chunk_size)
    assert isinstance(chunks, list)
    assert all(isinstance(chunk, str) for chunk in chunks)
    assert all(len(chunk) <= chunk_size for chunk in chunks)
