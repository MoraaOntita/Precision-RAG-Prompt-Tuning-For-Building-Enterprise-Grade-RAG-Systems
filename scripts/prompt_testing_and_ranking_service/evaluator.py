from langchain_openai import ChatOpenAI
import os
from langchain.schema import HumanMessage
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the LLM
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-4")

def evaluate_prompt(prompt: str) -> dict:
    try:
        human_message = HumanMessage(content=prompt)
        response = llm.invoke([human_message])
        return {'prompt': prompt, 'response': response.content}
    except Exception as e:
        logger.error(f"Error evaluating prompt '{prompt}': {e}")
        return {'prompt': prompt, 'response': None, 'error': str(e)}

def evaluate_test_cases(test_cases: list, max_workers: int = 5) -> list:
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(evaluate_prompt, case) for case in test_cases]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    return results

# Example usage
if __name__ == "__main__":
    test_cases = [
        "What is the main goal of the business need section?",
        "Describe the learning outcomes expected from this challenge.",
        "What are the deliverables for this week?",
        "Summarize the background context of this challenge.",
        "List the instructions provided for the submissions."
    ]

    # Evaluate test cases using the LLM
    evaluation_results = evaluate_test_cases(test_cases)
    for result in evaluation_results:
        prompt = result['prompt']
        response = result['response']
        error = result.get('error')
        if error:
            print(f"Test Case: {prompt}\nError: {error}\n")
        else:
            print(f"Test Case: {prompt}\nResult: {response}\n")
