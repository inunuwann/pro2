from unittest.mock import patch
import pytest
from src.models import Card, Player
from src.board import Board
from src.view import View

@pytest.fixture
def sample_board():
    players = [Player("テストプレイヤー"), Player("CPU", is_cpu=True)]
    view = View()
    return Board(players, view)

def test_choose_card(sample_board):
    player = sample_board.players[0]
    card = Card(1, "光")
    player.hand.append(card)

    with patch("builtins.input", return_value="0"):  # モックで入力を自動化
        chosen_card = sample_board.choose_card(player)

    assert chosen_card == card
    assert chosen_card not in player.hand
