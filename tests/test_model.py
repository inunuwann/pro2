# tests/test_model.py

import pytest
from src.model import Card, Cardset

def test_generate_cards():
    cs = Cardset()
    cs.generate_cards()
    # 花札は通常48枚のカードである
    assert len(cs.cards) == 48

def test_check_yaku():
    # 例：5枚の「光」カードで「五光」が成立するかテスト
    cards = [Card(1, "光"), Card(3, "光"), Card(8, "光"), Card(11, "光"), Card(12, "光")]
    cs = Cardset(cards)
    yaku = cs.check_yaku()
    assert "五光" in yaku

