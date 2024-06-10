import pytest
from scripts.automate_evaluation_service.evaluation_service import evaluate_prompt, evaluate_test_cases, generate_report

def test_evaluate_prompt():
    prompt = "Generate a summary for the business need section."
    test_case = "What is the main goal of the business need section?"
    score = evaluate_prompt(prompt, test_case)
    assert 0 <= score <= 1  # Assuming the score is between 0 and 1

def test_evaluate_test_cases():
    test_cases = ["Test case 1", "Test case 2"]
    prompts = ["Prompt 1", "Prompt 2"]
    results = evaluate_test_cases(test_cases, prompts)
    assert isinstance(results, dict)
    assert len(results) == len(prompts)

def test_generate_report():
    evaluation_results = {
        "Prompt 1": [0.8, 0.6],
        "Prompt 2": [0.4, 0.7]
    }
    report = generate_report(evaluation_results)
    assert "Prompt 1" in report
    assert "Average Score" in report
