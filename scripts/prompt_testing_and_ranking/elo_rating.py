from prompt import Prompt

def update_elo(winner, loser, k=32):
    """
    Update the ELO ratings for the winner and loser.

    :param winner: The Prompt instance that won the match.
    :param loser: The Prompt instance that lost the match.
    :param k: The K-factor, which determines the maximum possible adjustment per game.
    """
    expected_score_winner = 1 / (1 + 10 ** ((loser.elo_rating - winner.elo_rating) / 400))
    expected_score_loser = 1 / (1 + 10 ** ((winner.elo_rating - loser.elo_rating) / 400))
    
    winner.elo_rating += k * (1 - expected_score_winner)
    loser.elo_rating += k * (0 - expected_score_loser)

# Example usage:
if __name__ == "__main__":
    
    prompt1 = Prompt("Generate a summary for the business need section.")
    prompt2 = Prompt("Outline the key deliverables for this week.")

    print("Before match:")
    print(prompt1)
    print(prompt2)

    # Simulate a match where prompt1 wins against prompt2
    update_elo(prompt1, prompt2)

    print("After match:")
    print(prompt1)
    print(prompt2)
