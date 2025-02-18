import unittest
from card import Card, Cardset

class TestCardset(unittest.TestCase):
    def test_goko(self):
        cards = [
            Card(1, "光"), Card(3, "光"), Card(8, "光"),
            Card(11, "光"), Card(12, "光")
        ]
        cardset = Cardset(cards)
        self.assertEqual(cardset.check_yaku(), ["五光"])

    def test_shiko(self):
        cards = [
            Card(1, "光"), Card(3, "光"), Card(8, "光"),
            Card(12, "光")
        ]
        cardset = Cardset(cards)
        self.assertEqual(cardset.check_yaku(), ["四光"])

    def test_ame_shiko(self):
        cards = [
            Card(1, "光"), Card(3, "光"), Card(8, "光"),
            Card(11, "光")
        ]
        cardset = Cardset(cards)
        self.assertEqual(cardset.check_yaku(), ["雨四光"])

    def test_sanko(self):
        cards = [
            Card(3, "光"), Card(8, "光"), Card(12, "光")
        ]
        cardset = Cardset(cards)
        self.assertEqual(cardset.check_yaku(), ["三光"])

    def test_hanami_de_ippai(self):
        cards = [
            Card(3, "光"), Card(9, "タネ")
        ]
        cardset = Cardset(cards)
        self.assertEqual(cardset.check_yaku(), ["花見で一杯"])

    def test_tsukimi_de_ippai(self):
        cards = [
            Card(8, "光"), Card(9, "タネ")
        ]
        cardset = Cardset(cards)
        self.assertEqual(cardset.check_yaku(), ["月見で一杯"])

    def test_aotan(self):
        cards = [
            Card(6, "短冊"), Card(7, "短冊"), Card(9, "短冊")
        ]
        cardset = Cardset(cards)
        self.assertEqual(cardset.check_yaku(), ["青短"])

    def test_akatan(self):
        cards = [
            Card(1, "短冊"), Card(2, "短冊"), Card(3, "短冊")
        ]
        cardset = Cardset(cards)
        self.assertEqual(cardset.check_yaku(), ["赤短"])

def test_tan(self):
    cards = [
        Card(1, "短冊"), Card(2, "短冊"), Card(3, "短冊"),
        Card(4, "短冊"), Card(5, "短冊")
    ]
    cardset = Cardset(cards)
    self.assertEqual(set(cardset.check_yaku()), {"たん", "赤短"})

    def test_inosikacho(self):
        cards = [
            Card(6, "タネ"), Card(7, "タネ"), Card(10, "タネ")
        ]
        cardset = Cardset(cards)
        self.assertEqual(cardset.check_yaku(), ["猪鹿蝶"])

    def test_tane(self):
        cards = [
            Card(1, "タネ"), Card(2, "タネ"), Card(3, "タネ"),
            Card(4, "タネ"), Card(5, "タネ")
        ]
        cardset = Cardset(cards)
        self.assertEqual(cardset.check_yaku(), ["タネ"])

    def test_kasu(self):
        cards = [
            Card(1, "カス"), Card(2, "カス"), Card(3, "カス"),
            Card(4, "カス"), Card(5, "カス"), Card(6, "カス"),
            Card(7, "カス"), Card(8, "カス"), Card(9, "カス"),
            Card(10, "カス")
        ]
        cardset = Cardset(cards)
        self.assertEqual(cardset.check_yaku(), ["カス"])

if __name__ == '__main__':
    unittest.main()
