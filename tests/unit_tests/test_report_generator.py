# tests/test_report_generator.py
import pytest
from scripts.automate_evaluation_service.report_generator import generate_report

def test_generate_report():
    evaluation_results = [
        ("Test case 1", "Response 1"),
        ("Test case 2", "Response 2")
    ]
    report = generate_report(evaluation_results)
    assert "Test Case: Test case 1" in report
    assert "Response: Response 1" in report
