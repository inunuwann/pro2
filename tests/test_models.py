import pytest
from src.models import Card, Cardset

def test_card():
    card = Card(1, "光")
    assert card.month == 1
    assert card.kind == "光"
    assert str(card) == "1月の光"

def test_cardset_creation():
    card1 = Card(1, "光")
    card2 = Card(2, "短冊")
    cardset = Cardset([card1, card2])

    assert len(cardset.cards) == 2
    assert cardset.card_dict[1] == ["光"]
    assert cardset.card_dict[2] == ["短冊"]
    assert cardset.kind_dict["光"] == [1]
    assert cardset.kind_dict["短冊"] == [2]

def test_cardset_add_card():
    cardset = Cardset()
    card = Card(3, "カス")
    cardset.add_card(card)

    assert len(cardset.cards) == 1
    assert cardset.card_dict[3] == ["カス"]
    assert cardset.kind_dict["カス"] == [3]

def test_cardset_remove_card():
    card = Card(4, "タネ")
    cardset = Cardset([card])
    cardset.remove_card(card)

    assert len(cardset.cards) == 0
    assert 4 not in cardset.card_dict or not cardset.card_dict[4]  # 空リストもチェック
    assert "タネ" not in cardset.kind_dict or not cardset.kind_dict["タネ"]

def test_cardset_generate_cards():
    cardset = Cardset()
    cardset.generate_cards()

    assert len(cardset.cards) == 48  # 花札は合計48枚
