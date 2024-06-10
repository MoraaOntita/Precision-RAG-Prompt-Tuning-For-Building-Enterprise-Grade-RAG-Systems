# tests/test_integration.py
import os
import pytest
from docx import Document
from scripts.prompt_generation.retriever import retrieve_relevant_context
from scripts.prompt_generation.prompt_generator import generate_prompts
from scripts.automate_evaluation_service.evaluator import evaluate_test_cases
from scripts.automate_evaluation_service.report_generator import generate_report

# Sample document extraction function
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def test_integration():
    # Step 1: Extract text from document
    docx_path = "tests/test_data/sample_doc.docx"
    document_text = extract_text_from_docx(docx_path)
    assert len(document_text) > 0, "Document extraction failed"

    # Step 2: Generate prompts based on document text
    prompt = "Generate a summary for the business need section."
    relevant_contexts = retrieve_relevant_context(prompt)
    best_prompt, ranked_prompts = generate_prompts(prompt, relevant_contexts, os.getenv('OPENAI_API_KEY'))
    
    assert best_prompt is not None, "Prompt generation failed"
    assert len(ranked_prompts) > 0, "No ranked prompts generated"

    # Step 3: Evaluate the generated prompts
    test_cases = [
        "What is the main goal of the business need section?",
        "Describe the learning outcomes expected from this challenge.",
        "What are the deliverables for this week?",
        "Summarize the background context of this challenge.",
        "List the instructions provided for the submissions."
    ]
    evaluation_results = evaluate_test_cases(test_cases, [best_prompt] + ranked_prompts)
    
    assert len(evaluation_results) > 0, "Evaluation of prompts failed"
    
    # Step 4: Generate a report from the evaluation results
    report = generate_report(evaluation_results)
    assert "Test Case Evaluation Report" in report, "Report generation failed"
    
    # Optional: Print the report for visual inspection (not part of the assert checks)
    print(report)

if __name__ == "__main__":
    test_integration()
