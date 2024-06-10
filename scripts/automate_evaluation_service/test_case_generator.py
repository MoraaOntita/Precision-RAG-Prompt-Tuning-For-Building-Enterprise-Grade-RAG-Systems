import random
from typing import List, Union

def generate_random_test_case(length_range: tuple = (5, 20)) -> str:
    """
    Generate a random test case string of a random length within the given range.

    :param length_range: A tuple containing the minimum and maximum length of the generated string.
    :return: A random string.
    """
    length = random.randint(*length_range)
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))

def generate_scenario_based_test_case(scenario: str) -> str:
    """
    Generate a scenario-based test case.

    :param scenario: A string representing the scenario.
    :return: A test case string based on the scenario.
    """
    scenarios = {
        # Technical document scenarios
        'business_need': [
            "What is the business need for this week's challenge?",
            "Describe the business context of the current project.",
            "Why is this project important from a business perspective?"
        ],
        'background_context': [
            "Provide some background context for this project.",
            "What is the historical context of this challenge?",
            "Explain the background information relevant to this project."
        ],
        'learning_outcome': [
            "What are the expected learning outcomes for this challenge?",
            "Describe the skills and knowledge participants should gain.",
            "What should participants learn from this project?"
        ],
        'team': [
            "Who are the team members for this project?",
            "Describe the roles of each team member.",
            "How is the team structured for this challenge?"
        ],
        'badges': [
            "What badges can participants earn from this challenge?",
            "Describe the criteria for earning badges.",
            "What are the different types of badges available?"
        ],
        'group_work_policy': [
            "What is the group work policy for this challenge?",
            "Explain the rules for collaborating on this project.",
            "How should team members interact according to the group work policy?"
        ],
        'instructions': [
            "Provide detailed instructions for completing this challenge.",
            "What are the step-by-step instructions for this project?",
            "Describe the instructions participants need to follow."
        ],
        'tutorials_schedule': [
            "What is the schedule for the tutorials?",
            "Provide the tutorial schedule for this week.",
            "When are the tutorials for this project scheduled?"
        ],
        'deliverables': [
            "What are the deliverables for this week's challenge?",
            "Describe the required deliverables for this project.",
            "What should participants submit as deliverables?"
        ],
        'references': [
            "What references should participants use for this challenge?",
            "Provide a list of references for this project.",
            "What resources are recommended for this challenge?"
        ],
        
        # Non-technical document scenarios
        'introduction': [
            "Provide an introduction for the career challenge.",
            "What is the scenario for this career challenge?",
            "Describe the introduction or scenario of this task."
        ],
        'exercise': [
            "What exercise is required in this career challenge?",
            "Describe the exercise participants need to complete.",
            "What is the main task in this exercise?"
        ],
        'questions_to_reflect_on': [
            "What questions should participants reflect on?",
            "List the questions for reflection in this challenge.",
            "What are the reflection questions for this task?"
        ],
        'deliverables_career': [
            "What are the deliverables for this career challenge?",
            "Describe the deliverables required for this task.",
            "What should participants submit for the career challenge?"
        ],
        'rubrics': [
            "What is the rubric for evaluating this challenge?",
            "Describe the evaluation criteria for this task.",
            "How will the deliverables be assessed?"
        ],
        'instructions_for_submission': [
            "What are the instructions for submitting the deliverables?",
            "Describe the submission process for this challenge.",
            "How should participants submit their work?"
        ],
        'deadlines': [
            "What is the deadline for this challenge?",
            "Provide the deadlines for the deliverables.",
            "When should participants submit their work?"
        ]
    }

    return random.choice(scenarios.get(scenario, ["This is a default test case."]))

def generate_test_cases(num_random_cases: int = 10, scenario: str = 'default') -> List[str]:
    """
    Generate a list of test cases including random and scenario-based cases.

    :param num_random_cases: Number of random test cases to generate.
    :param scenario: Scenario for generating scenario-based test case.
    :return: A list of generated test cases.
    """
    test_cases = [generate_random_test_case() for _ in range(num_random_cases)]
    test_cases.append(generate_scenario_based_test_case(scenario))
    return test_cases

# Example usage
if __name__ == "__main__":
    random_cases = generate_test_cases(num_random_cases=5, scenario='deliverables')
    for case in random_cases:
        print(case)
