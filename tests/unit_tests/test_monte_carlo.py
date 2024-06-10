import pytest
from scripts.prompt_testing_and_ranking.prompt import Prompt
from scripts.prompt_testing_and_ranking.monte_carlo import simulate_match, monte_carlo_matchmaking

def test_simulate_match():
    prompt1 = Prompt("Prompt 1")
    prompt2 = Prompt("Prompt 2")
    winner, loser = simulate_match(prompt1, prompt2)
    assert (winner == prompt1 and loser == prompt2) or (winner == prompt2 and loser == prompt1)

def test_monte_carlo_matchmaking():
    prompts = [Prompt(f"Prompt {i}") for i in range(10)]
    monte_carlo_matchmaking(prompts, num_simulations=10)
    for prompt in prompts:
        assert prompt.elo_rating != 1000 
