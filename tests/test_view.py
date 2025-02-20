import pytest
from unittest.mock import patch
from src.view import View

@pytest.fixture
def sample_view():
    return View()

def test_display_message(sample_view, capsys):
    sample_view.display_message("テストメッセージ")
    captured = capsys.readouterr()
    assert "テストメッセージ" in captured.out

def test_choose_from_list(sample_view):
    items = ["選択肢1", "選択肢2"]
    with patch("builtins.input", return_value="0"):
        choice = sample_view.choose_from_list("選んでください:", items)
        assert choice == 0
