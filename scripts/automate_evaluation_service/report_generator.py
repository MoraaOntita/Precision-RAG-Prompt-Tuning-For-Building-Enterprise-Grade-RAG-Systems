import json
from typing import Dict, List

def generate_report(evaluation_results: Dict[str, List[float]]) -> str:
    report_lines = []
    report_lines.append("Test Case Evaluation Report\n")
    report_lines.append("="*80 + "\n")

    for prompt, scores in evaluation_results.items():
        avg_score = sum(scores) / len(scores)
        report_lines.append(f"Prompt: {prompt}\n")
        report_lines.append(f"Average Score: {avg_score:.2f}\n")
        report_lines.append(f"Scores: {', '.join(f'{score:.2f}' for score in scores)}\n")
        report_lines.append("-"*80 + "\n")

    return "\n".join(report_lines)

def save_report_to_file(report: str, filename: str) -> None:
    with open(filename, 'w') as file:
        file.write(report)

def save_results_to_json(evaluation_results: Dict[str, List[float]], filename: str) -> None:
    with open(filename, 'w') as file:
        json.dump(evaluation_results, file, indent=4)

# Example usage
if __name__ == "__main__":
    evaluation_results = {
        "Generate a summary for the business need section.": [0.82, 0.75, 0.88, 0.79, 0.81],
        "Outline the key deliverables for this week.": [0.89, 0.85, 0.87, 0.90, 0.86],
        "What are the main learning outcomes of this challenge?": [0.78, 0.77, 0.79, 0.80, 0.76],
        "Summarize the background context and objectives of the project.": [0.84, 0.83, 0.82, 0.85, 0.81]
    }

    # Generate and save report
    report = generate_report(evaluation_results)
    print(report)
    save_report_to_file(report, "evaluation_report.txt")
    save_results_to_json(evaluation_results, "evaluation_results.json")
