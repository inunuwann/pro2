import pytest
from unittest.mock import patch
from src.models import Player
from src.view import View
from src.controller import Controller

@pytest.fixture
def sample_controller():
    players = [Player("あなた"), Player("CPU", is_cpu=True)]
    view = View()
    return Controller(players, view)

def test_controller_initialization(sample_controller):
    assert len(sample_controller.board.players) == 2

def test_run_game(sample_controller):
    with patch.object(sample_controller.board, "setup_round", return_value=(1, [])), \
         patch.object(sample_controller.board, "play_turn", return_value=(True, [])), \
         patch.object(sample_controller, "show_game_result"):

        sample_controller.run_game()
