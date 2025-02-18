# tests/test_controller.py

import pytest
from src.model import Player
from src.controller import Controller
from src.view import DummyView

def test_run_game_cpu():
    # CPU 対戦でゲームを実行
    cpu1 = Player("CPU1", is_cpu=True)
    cpu2 = Player("CPU2", is_cpu=True)
    players = [cpu1, cpu2]
    dummy_view = DummyView()
    controller = Controller(players, dummy_view)
    controller.run_game()
    # ゲーム終了時に両プレイヤーが何らかのカードを獲得していることを確認
    assert len(cpu1.captured) > 0
    assert len(cpu2.captured) > 0

