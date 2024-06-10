# tests/test_app.py
import pytest
from streamlit.testing import StreamlitTestRunner

def test_app_functionality():
    runner = StreamlitTestRunner("app.py")
    runner.start()
    page = runner.page()
    
    assert page.title == "Prompt Generation Tool"

    document_selector = page.get_by_label("Select a document")
    assert document_selector.exists()

    document_selector.select_option("Sample Document.docx")
    page.get_by_text("Document Content")
    assert "Sample Document Content" in page.get_text_area_content()

    page.get_by_label("Enter your prompt for Sample Document.docx").fill("Generate a summary")
    page.get_by_label("Enter the expected output for Sample Document.docx").fill("Summary of the document")

    save_button = page.get_by_text("Save Prompt for Sample Document.docx")
    assert save_button.exists()
    save_button.click()

    assert "Prompt for Sample Document.docx saved!" in page.get_alert_text()

    generate_button = page.get_by_text("Generate and Rank Prompts")
    assert generate_button.exists()
    generate_button.click()

    assert "Best Generated Prompt" in page.get_text_area_content()
    assert "All Ranked Prompts" in page.get_text_area_content()
