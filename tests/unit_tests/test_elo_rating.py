# tests/test_elo_rating.py
import pytest
from scripts.prompt_testing_and_ranking.elo_rating import update_elo
from scripts.prompt_testing_and_ranking.prompt import Prompt

def test_update_elo():
    winner = Prompt("Winner")
    loser = Prompt("Loser")
    winner_initial_rating = winner.elo_rating
    loser_initial_rating = loser.elo_rating
    update_elo(winner, loser)
    assert winner.elo_rating > winner_initial_rating
    assert loser.elo_rating < loser_initial_rating
