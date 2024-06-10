import pytest
from scripts.automate_evaluation_service.evaluator import evaluate_test_cases

def test_evaluate_test_cases():
    test_cases = [
        "What is the main goal of the business need section?",
        "Describe the learning outcomes expected from this challenge."
    ]
    results = evaluate_test_cases(test_cases)
    assert isinstance(results, list)
    assert len(results) == len(test_cases)
    for case, result in results:
        assert isinstance(case, str)
        assert isinstance(result, str)
