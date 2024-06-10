import random
from typing import List, Tuple
import logging
from prompt import Prompt
from elo_rating import update_elo 

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def simulate_match(prompt1: Prompt, prompt2: Prompt) -> Tuple[Prompt, Prompt]:
    """Simulates a match between two prompts and returns the winner and loser."""
    if not isinstance(prompt1, Prompt) or not isinstance(prompt2, Prompt):
        raise ValueError("Both arguments must be instances of the Prompt class.")
    
    score1 = random.uniform(0, 1)
    score2 = random.uniform(0, 1)
    if score1 > score2:
        return prompt1, prompt2
    else:
        return prompt2, prompt1

def monte_carlo_matchmaking(prompts: [List<Prompt], num_simulations: int):
    
    """
    Performs Monte Carlo matchmaking simulations and updates ELO ratings.
    """
    
    if not isinstance(prompts, list) or not all(isinstance(prompt, Prompt) for prompt in prompts):
        raise ValueError("Prompts must be a list of Prompt instances.")
    if not isinstance(num_simulations, int) or num_simulations <= 0:
        raise ValueError("Number of simulations must be a positive integer.")
    
    logger.info(f"Starting Monte Carlo matchmaking with {num_simulations} simulations.")

    for i in range(num_simulations):
        prompt1, prompt2 = random.sample(prompts, 2)
        winner, loser = simulate_match(prompt1, prompt2)
        update_elo(winner, loser)
        logger.debug(f"Simulation {i+1}: {winner} won against {loser}")

    logger.info("Monte Carlo matchmaking completed.")

# Example usage
if __name__ == "__main__":
    prompts = [
        Prompt("Generate a summary for the business need section."),
        Prompt("Outline the key deliverables for this week."),
        Prompt("What are the main learning outcomes of this challenge?"),
        Prompt("Summarize the background context and objectives of the project.")
    ]
    
    num_simulations = 100
    monte_carlo_matchmaking(prompts, num_simulations)

    for prompt in prompts:
        print(prompt)
