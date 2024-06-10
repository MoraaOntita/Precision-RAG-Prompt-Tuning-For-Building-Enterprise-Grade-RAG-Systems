import random
from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Initialize the Sentence Transformer model for semantic similarity evaluation
model = SentenceTransformer('all-MiniLM-L6-v2')

def evaluate_prompt(prompt: str, test_case: str) -> float:
    """
    Evaluate the given prompt against a test case using cosine similarity.

    Args:
        prompt (str): The generated prompt.
        test_case (str): The test case for evaluation.

    Returns:
        float: The evaluation score based on cosine similarity.
    """
    prompt_embedding = model.encode(prompt, convert_to_tensor=True)
    test_case_embedding = model.encode(test_case, convert_to_tensor=True)
    similarity_score = cosine_similarity([prompt_embedding], [test_case_embedding])[0][0]
    return similarity_score

def evaluate_test_cases(test_cases: List[str], prompts: List[str]) -> Dict[str, List[float]]:
    """
    Evaluate multiple prompts against a set of test cases.

    Args:
        test_cases (List[str]): The list of test cases.
        prompts (List[str]): The list of generated prompts.

    Returns:
        Dict[str, List[float]]: A dictionary containing evaluation results.
    """
    evaluation_results = {}
    for prompt in prompts:
        scores = [evaluate_prompt(prompt, test_case) for test_case in test_cases]
        evaluation_results[prompt] = scores
    return evaluation_results

def generate_report(evaluation_results: Dict[str, List[float]]) -> str:
    """
    Generate a report summarizing the evaluation results.

    Args:
        evaluation_results (Dict[str, List[float]]): The evaluation results.

    Returns:
        str: The generated report as a string.
    """
    report_lines = []
    for prompt, scores in evaluation_results.items():
        avg_score = sum(scores) / len(scores)
        report_lines.append(f"Prompt: {prompt}\nAverage Score: {avg_score:.2f}\nScores: {scores}\n")
    return "\n".join(report_lines)

# Example usage
if __name__ == "__main__":
    # Example prompts and test cases
    test_cases = [
        "What is the main goal of the business need section?",
        "Describe the learning outcomes expected from this challenge.",
        "What are the deliverables for this week?",
        "Summarize the background context of this challenge.",
        "List the instructions provided for the submissions."
    ]

    prompts = [
        "Generate a summary for the business need section.",
        "Outline the key deliverables for this week.",
        "What are the main learning outcomes of this challenge?",
        "Summarize the background context and objectives of the project."
    ]

    # Evaluate and generate report
    try:
        evaluation_results = evaluate_test_cases(test_cases, prompts)
        report = generate_report(evaluation_results)
        print(report)
    except Exception as e:
        print(f"An error occurred during the evaluation process: {e}")
